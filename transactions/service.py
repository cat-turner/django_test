from typing import Dict

from django.db.utils import IntegrityError

from transactions import models
from transactions.enums import TransactionType
from utils.time_conversions import get_utc_time


class TransactionService:
    def parse_line_from_dict(self, line: Dict) -> models.FBATransaction:

        transaction_type = TransactionType.text_to_enum(line["type"]).value

        # save the description
        sku = line["sku"].lower() if line["sku"] else None
        description_text = line["description"].lower() if line["description"] else None

        try:
            td = models.TransactionDescription(
                description_text=description_text, sku=sku
            )
            td.save()
        except IntegrityError:
            td = models.TransactionDescription.objects.get(
                description_text=description_text, sku=sku
            )
        order_id = line["order id"]

        date = get_utc_time(line["date/time"])
        city = line["order city"]
        state = line["order state"]
        postal = line["order postal"] if line["order postal"] else None
        total = line["total"] if line["total"] else None
        qty = int(line["quantity"]) if line["quantity"] else 0

        # simple check to avoid dupes
        if order_id and transaction_type != TransactionType.NOT_DEFINED:
            # update instead of create
            transaction, _ = models.FBATransaction.objects.update_or_create(
                order_id=order_id,
                type=transaction_type,
                date=date,
                defaults={
                    "date": date,
                    "transaction_description": td,
                    "type": transaction_type,
                    "order_id": order_id,
                    "quantity": qty,
                    "sku": sku,
                    "total": total,
                    "city": city,
                    "state": state,
                    "postal": postal,
                },
            )

        else:
            # always create if no defined order id
            transaction = models.FBATransaction(
                date=date,
                transaction_description=td,
                type=transaction_type,
                order_id=order_id,
                quantity=qty,
                sku=sku,
                total=total,
                city=city,
                state=state,
                postal=postal,
            )
            transaction.save()
        return transaction
