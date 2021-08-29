from __future__ import annotations

from enum import Enum
from typing import List, Optional


class TransactionTypeParseError(ValueError):
    pass


class TransactionType(Enum):
    """
    A class that defines supported transaction types. Can be used in models or outside of models.
    """

    NOT_DEFINED = "NOT_DEFINED"
    ORDER = "ORDER"
    FBA_INVENTORY_FEE = "FBA_INVENTORY_FEE"
    ADJUSTMENT = "ADJUSTMENT"
    FBA_CUSTOMER_RETURN_FEE = "FBA_CUSTOMER_RETURN_FEE"
    REFUND = "REFUND"
    TRANSFER = "TRANSFER"
    ORDER_RETROCHARGE = "ORDER_RETROCHARGE"

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
            "fba customer return fee": TransactionType.FBA_CUSTOMER_RETURN_FEE,
            "refund": TransactionType.REFUND,
            "transfer": TransactionType.TRANSFER,
            "order retrocharge": TransactionType.ORDER_RETROCHARGE,
            "order_retrocharge": TransactionType.ORDER_RETROCHARGE,
            "not_defined": TransactionType.NOT_DEFINED,
            "fba_inventory_fee": TransactionType.FBA_INVENTORY_FEE,
            "adjustment": TransactionType.ADJUSTMENT,
            "fba_customer_return_fee": TransactionType.FBA_CUSTOMER_RETURN_FEE,
        }
        match = map_enum.get(text)
        if not match:
            raise TransactionTypeParseError(f"Cannot find enum from string - {text}")
        return match
