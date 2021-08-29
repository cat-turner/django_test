import re
# Create your models here.
# https://docs.djangoproject.com/en/3.1/topics/db/models/
# After writing model definition, run "./manage.py makemigrations" and then "./manage.py migrate"
from decimal import Decimal
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models

from transactions.enums import TransactionType
from utils.us_states import STATES_NORMALIZED


class MoneyField(models.IntegerField):
    description = "Use an integer & store the prices as the lowest common unit, but act like a float"

    def get_db_prep_value(self, value, *args, **kwargs) -> Optional[int]:
        if value is None:
            return None
        return int(round(Decimal(value) * 100))

    def to_python(self, value) -> Optional[Decimal]:
        if value is None or isinstance(value, Decimal):
            return value
        try:
            return Decimal(value) / 100
        except (TypeError, ValueError):
            raise ValidationError(
                "This value must be an integer or a string represents an integer."
            )

    def from_db_value(
        self, value, expression, connection, context=None
    ) -> Optional[Decimal]:
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {"form_class": models.DecimalField}
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)


class StateField(models.CharField):
    description = "A field that normalizes a state name if it is in US. If not, saves it in the original form"

    def get_db_prep_value(self, value: Optional[str], *args, **kwargs) -> Optional[str]:
        if value is None:
            return None
        value = value.lower()
        # if org value returned it means
        # that value is likely not a US state, save as-is
        result = STATES_NORMALIZED.get(value, value)
        return result.lower()


class CharNormalizedField(models.CharField):
    description = "A field that will always be saved as lowercase"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        return str(value).lower()


class TransactionDescription(models.Model):
    """
    Descriptions used in FBATransaction
    """

    class Meta:
        # added a unique constrain that includes the sku and description so to avoid duplicating
        # skus with the same description
        constraints = [
            models.UniqueConstraint(
                fields=["description_text", "sku"],
                name="unique_transaction_description",
            )
        ]

    # char limit set to 200 but it can be bumped to something higher
    description_text = models.CharField(max_length=200, null=True, blank=True)
    sku = CharNormalizedField(max_length=100, null=True, blank=True)


def validate_zip(input: Optional[str]) -> None:
    if not input:
        return None
    z = re.match("^\d{5}(?:-\d{4})?$", input)
    if not z:
        raise ValidationError("Zip input fails validation")


class FBATransaction(models.Model):
    """
    A single transaction from the FBA transaction report download
    """

    class Meta:
        db_table = "fba_transactions"

    date = models.DateTimeField(null=False, blank=False)

    # Allow restrictions without an exception because this information is not important
    transaction_description = models.ForeignKey(
        TransactionDescription, on_delete=models.SET_NULL, null=True
    )
    # Set default to TransactionType.NOT_DEFINED if the model does not have a type
    type = models.CharField(
        choices=TransactionType.choices(),
        default=TransactionType.NOT_DEFINED,
        max_length=50,
    )
    order_id = CharNormalizedField(max_length=32, null=True, blank=True)

    quantity = models.IntegerField(null=True, blank=True)

    # I repeat this field so that I can do a lookup without joins
    sku = CharNormalizedField(max_length=100, null=True, blank=True)
    total = MoneyField(null=True, blank=True)
    city = CharNormalizedField(max_length=100, null=True, blank=True)
    state = StateField(max_length=100, null=True, blank=True)
    postal = models.CharField(
        max_length=10, null=True, blank=True, validators=[validate_zip]
    )
