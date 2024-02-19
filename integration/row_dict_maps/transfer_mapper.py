from integration.system.RowDictMapper import RowDictMapper
from database import models
from flask import request, jsonify
from sqlalchemy import Column

class TransferMapper(RowDictMapper):
    """ Format

    Map Transfer row into dict for sending as Kafka message

    Returns:
        _type_: RowDictMapper object
    """
    
    def __init__(self):
        """ Format

        Map Transfer tow into dict for sending as Kafka message

        TODO: pass Customer.Name (a join field)

        Returns:
            _type_: RowDictMapper object
        """
        transfer = super(TransferMapper, self).__init__(
            model_class=models.Transfer
            , alias = "transfer"
            , fields = [ models.Transfer.FromAccountID, models.Transfer.ToAccountID,
                        models.Transfer.TransactionDate, models.Transfer.Amount
                    ]
            )
        

        return transfer
