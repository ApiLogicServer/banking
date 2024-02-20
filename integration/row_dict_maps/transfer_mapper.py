from integration.system.RowDictMapper import RowDictMapper
from database import models
from flask import request, jsonify
from sqlalchemy import Column
from logic_bank.exec_row_logic.logic_row import LogicRow

class TransferMapper(RowDictMapper):
    """ Format

    Map Transfer row into dict for sending as Kafka message

    Returns:
        _type_: RowDictMapper object
    """
    
    def __init__(self, logic_row: LogicRow = None):
        """ Format

        Map Transfer row into dict for sending as Kafka message

        Note: declare Customer.FirstName (a join field)

        Returns:
            _type_: RowDictMapper object
        """
        transfer = super(TransferMapper, self).__init__(
            model_class=models.Transfer
            , logic_row=logic_row
            , alias = "transfer"
            , fields = [ (logic_row.row.Account.Customer.FirstName, "First"),
                        (logic_row.row.Account.Customer.LastName, "Last"),
                        models.Transfer.FromAccountID, models.Transfer.ToAccountID,
                        models.Transfer.TransactionDate, models.Transfer.Amount
                    ]
            )
        return transfer
