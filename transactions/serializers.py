from decimal import Decimal
from typing import Optional

from rest_framework import serializers

from transactions.enums import TransactionType
from transactions.models import FBATransaction


class FBATransactionSerializer(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    def get_total(self, obj) -> Optional[Decimal]:
        return Decimal(obj.total)

    class Meta:
        model = FBATransaction
        exclude = ["transaction_description"]
