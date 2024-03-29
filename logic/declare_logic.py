import datetime
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from database import models
import api.system.opt_locking.opt_locking as opt_locking
from security.system.authorization import Grant
import logging
from datetime import date
import safrs
import json
import requests
from confluent_kafka import Producer, KafkaException
import integration.kafka.kafka_producer as kafka_producer
from integration.row_dict_maps.transfer_mapper import TransferMapper
from config.config import Args
import socket

app_logger = logging.getLogger(__name__)

declare_logic_message = "*** Banking Rules Loaded ***"  # printed in api_logic_server.py
db = safrs.DB 
session = db.session 
producer = None
conf = None
    
def declare_logic():
    ''' Declarative multi-table derivations and constraints, extensible with Python. 

    Brief background: see readme_declare_logic.md
    
    Use code completion (Rule.) to declare rules here:
    '''
    
    Rule.sum(derive=models.Account.AcctBalance, 
                as_sum_of=models.TransactionLog.TotalAmount)
    
    Rule.constraint(validate=models.Account, 
                as_condition=lambda row: row.AcctBalance >= 0,
                error_msg="Account balance {row.AcctBalance} cannot be less than zero")
        
    Rule.formula(derive=models.TransactionLog.TotalAmount,
                as_expression=lambda row: row.Deposit - row.Withdrawl)
    
    Rule.constraint(validate=models.TransactionLog, 
                as_condition=lambda row: row.Deposit >= 0,
                error_msg="Deposit {row.Deposit} must be a positive amount")
    
    Rule.constraint(validate=models.TransactionLog, 
                as_condition=lambda row: row.Withdrawl >= 0,
                error_msg="Withdrawl {row.Withdrawl} must be a positive amount")
    
    Rule.constraint(validate=models.Transfer, 
                as_condition=lambda row: row.FromAccountID != row.ToAccountID,
                error_msg="FromAccount {row.FromAccountID} must be different from ToAccount {row.ToAccountID}")


    def fn_transfer_funds(row=models.Transfer, old_row=models.Transfer, logic_row=LogicRow):
        """
        Creates 2 TransactionLog rows (from/to account), which adjust Customers' Account.AcctBalance

        Args:
            row (_type_, optional): _description_. Defaults to models.Transfer.
            old_row (_type_, optional): _description_. Defaults to models.Transfer.
            logic_row (_type_, optional): _description_. Defaults to LogicRow.

        Raises:
            requests.RequestException: _description_
            requests.RequestException: _description_
            requests.RequestException: _description_
        """
        if logic_row.ins_upd_dlt != "ins":
            return
        fromAcctId = row.FromAccountID
        toAcctId = row.ToAccountID
        amount = row.Amount
        
        transactions = session.query(models.TransactionLog).all()
        try:
            from_account = session.query(models.Account).filter(models.Account.AccountID == fromAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"From Account {fromAcctId} not found"
            ) from ex
            
        try:
            to_account = session.query(models.Account).filter(models.Account.AccountID == toAcctId).one()
        except Exception as ex:
            raise requests.RequestException(
                f"To Account {toAcctId} not found"
            ) from ex
        
        if from_account.Customer != to_account.Customer:
            raise requests.RequestException(
                f"FromAccount Customer {from_account.Customer} must be the same as the ToAccount Customer {to_account.Customer}"
            ) from ex
        
        if from_account.AcctBalance > amount:
            # #Not Enough Funds - if Loan exists move to cover Overdraft (transfer Loan to from_acct)
            pass
            
        from_trans = logic_row.new_logic_row(models.TransactionLog)
        from_trans.row.TransactionID = len(transactions) + 2    # Val: yank?
        from_trans.row.AccountID = fromAcctId
        from_trans.row.Withdrawl = amount
        from_trans.row.TransactionType = "Transfer From"
        # from_trans.row.TransactionDate = date.today()           # yank?
        from_trans.insert(reason="Transfer From")
        
        to_trans = logic_row.new_logic_row(models.TransactionLog)
        to_trans.row.TransactionID = len(transactions) + 3
        to_trans.row.AccountID = toAcctId
        to_trans.row.Deposit = amount
        to_trans.row.TransactionType = "Transfer To"
        # to_trans.row.TransactionDate = date.today()
        to_trans.insert(reason="Transfer To")
        
        logic_row.log("Funds transferred successfully!")

    def fn_send_kafka_message(row: models.Transfer, old_row: models.Transfer, logic_row: LogicRow):
        """ #als: Send Kafka message formatted by TransferMapper RowDictMapper

        Format row per requirements, and send (e.g., a message)

        NB: the after_flush event makes autonum attrs available.

        Args:
            row (models.Order): inserted Order
            old_row (models.Order): n/a
            logic_row (LogicRow): bundles curr/old row, with ins/upd/dlt logic
        """
        if logic_row.is_inserted():
            kafka_producer.send_kafka_message(logic_row=logic_row,
                                              row_dict_mapper=TransferMapper,
                                              kafka_topic="Transfer",
                                              kafka_key=str(row.TransactionID),
                                              msg="Sending Funds Transfer")

    Rule.commit_row_event(on_class=models.Transfer, calling=fn_transfer_funds)

    Rule.after_flush_row_event(on_class=models.Transfer, calling=fn_send_kafka_message)

    def handle_all(logic_row: LogicRow):  # OPTIMISTIC LOCKING, [TIME / DATE STAMPING]
        """
        This is generic - executed for all classes.

        Invokes optimistic locking.

        You can optionally do time and date stamping here, as shown below.

        Args:
            logic_row (LogicRow): from LogicBank - old/new row, state
        """
        global producer,conf
        if Args.instance.kafka_producer:
            conf = Args.instance.kafka_producer
            if "client.id" not in conf:
                conf["client.id"] = socket.gethostname()
            # conf = {'bootstrap.servers': 'localhost:9092', 'client.id': socket.gethostname()}
            producer = Producer(conf)
            app_logger.debug(f'\nKafka producer connected')
        
        #This will enable declarative role based access 
        Grant.process_updates(logic_row=logic_row)
        
        if logic_row.is_updated() and logic_row.old_row is not None and logic_row.nest_level == 0:
            opt_locking.opt_lock_patch(logic_row=logic_row)
        
        enable_creation_stamping = True  # OpenDate time stamping
        if enable_creation_stamping:
            row = logic_row.row
            if logic_row.ins_upd_dlt == "ins" and hasattr(row, "OpenDate"):
                row.OpenDate = datetime.datetime.now()
                logic_row.log("early_row_event_all_classes - handle_all sets 'OpenDate"'')
        
    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)


    declare_logic_message = "..logic/declare_logic.py (logic == rules + code)"
    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

