from __future__ import annotations

from enum import IntEnum
from typing import Optional, List

class TransactionTypeParseError(ValueError):
    pass

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
    def choices(cls) -> List:
        return [(key.value, key.name) for key in cls]

    @classmethod
    def text_to_enum(cls, text: Optional[str] = None) -> TransactionType:
        if not text:
            return TransactionType.NOT_DEFINED
        text = text.lower()
        map_enum = {
            "order": TransactionType.ORDER,
            "fba inventory fee": TransactionType.FBA_INVENTORY_FEE,
            "adjustment": TransactionType.ADJUSTMENT,
            "fda customer return fee": TransactionType.FBA_CUSTOMER_RETURN_FEE,
            "refund": TransactionType.REFUND,
            "transfer": TransactionType.TRANSFER,
            "order_retrocharge": TransactionType.ORDER_RETROCHARGE,
        }
        match = map_enum.get(text)
        if not match:
            raise TransactionTypeParseError(f"Cannot find enum from string - {text}")
        return match
