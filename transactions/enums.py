from enum import IntEnum
from typing import Optional


class TransactionType(IntEnum):
    """
    A class that defines supported transaction types. Can be used in models or outside of models.
    """

    NOT_DEFINED = 0
    ORDER = 1
    FBA_INVENTORY_FEE = 2
    ADJUSTMENT = 3
    FBA_CUSTOMER_RETURN_FEE = 4
    REFUND = 5
    TRANSFER = 6
    ORDER_RETROCHARGE = 7

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def text_to_enum(cls, text: Optional[str] = None):
        if not text:
            return TransactionType.NOT_DEFINED

        map_enum = {
            "Order": TransactionType.ORDER,
            "FBA Inventory Fee": TransactionType.FBA_INVENTORY_FEE,
            "Adjustment": TransactionType.ADJUSTMENT,
            "FBA Customer Return Fee": TransactionType.FBA_CUSTOMER_RETURN_FEE,
            "Refund": TransactionType.REFUND,
            "Transfer": TransactionType.TRANSFER,
            "Order_Retrocharge": TransactionType.ORDER_RETROCHARGE,
        }
        match = map_enum.get(text)
        if not match:
            raise ValueError("Cannot find enum from string")
        return match
