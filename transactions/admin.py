from django.contrib import admin

# Register your models here.
from transactions.models import FBATransaction, TransactionDescription

admin.site.register(FBATransaction)
admin.site.register(TransactionDescription)
