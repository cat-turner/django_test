# Generated by Django 3.1.2 on 2021-08-29 02:50

from django.db import migrations, models
import django.db.models.deletion
import transactions.enums
import transactions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FBATransaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("NOT_DEFINED", "NOT_DEFINED"),
                            ("ORDER", "ORDER"),
                            ("FBA_INVENTORY_FEE", "FBA_INVENTORY_FEE"),
                            ("ADJUSTMENT", "ADJUSTMENT"),
                            ("FBA_CUSTOMER_RETURN_FEE", "FBA_CUSTOMER_RETURN_FEE"),
                            ("REFUND", "REFUND"),
                            ("TRANSFER", "TRANSFER"),
                            ("ORDER_RETROCHARGE", "ORDER_RETROCHARGE"),
                        ],
                        default=transactions.enums.TransactionType["NOT_DEFINED"],
                        max_length=50,
                    ),
                ),
                (
                    "order_id",
                    transactions.models.CharNormalizedField(
                        blank=True, max_length=32, null=True
                    ),
                ),
                ("quantity", models.IntegerField(blank=True, null=True)),
                (
                    "sku",
                    transactions.models.CharNormalizedField(
                        blank=True, max_length=100, null=True
                    ),
                ),
                ("total", transactions.models.MoneyField(blank=True, null=True)),
                (
                    "city",
                    transactions.models.CharNormalizedField(
                        blank=True, max_length=100, null=True
                    ),
                ),
                (
                    "state",
                    transactions.models.StateField(
                        blank=True, max_length=100, null=True
                    ),
                ),
                (
                    "postal",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        validators=[transactions.models.validate_zip],
                    ),
                ),
            ],
            options={
                "db_table": "fba_transactions",
            },
        ),
        migrations.CreateModel(
            name="TransactionDescription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description_text",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "sku",
                    transactions.models.CharNormalizedField(
                        blank=True, max_length=100, null=True
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="transactiondescription",
            constraint=models.UniqueConstraint(
                fields=("description_text", "sku"),
                name="unique_transaction_description",
            ),
        ),
        migrations.AddField(
            model_name="fbatransaction",
            name="transaction_description",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="transactions.transactiondescription",
            ),
        ),
    ]
