import datetime

from django.db import models
from django_db_views.db_view import DBView
from utils.query_builder import MASTER_LEDGER_VIEW
import uuid


class TransactionType(models.TextChoices):
    CREDIT = 'credit'
    DEBIT = 'debit'


class FiscalTerm(models.Model):
    semester = models.CharField(default=" ")
    start_date = models.DateField(default=datetime.datetime.now)
    end_date = models.DateField(default=datetime.datetime.now)
    notes = models.TextField(default="Blank")


class TransactionCategory(models.Model):
    category = models.CharField(default=" ")
    value = models.CharField(default=" ")


class Budget(models.Model):
    fiscal = models.ForeignKey(FiscalTerm, on_delete=models.CASCADE)
    category_id = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    budget = models.FloatField(default=0.0)


class CashLedger(models.Model):
    fiscal = models.ForeignKey(FiscalTerm, on_delete=models.CASCADE)
    budget = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, related_name='cash_budget_transactions')
    purpose = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, related_name='cash_purpose_transactions')
    transaction_id = models.UUIDField(default=uuid.uuid4)
    date = models.DateField(default=datetime.datetime.now)
    amount = models.FloatField(default=0.0)
    details = models.TextField(default="Blank")
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices, default=TransactionType.CREDIT)
    account = models.CharField(max_length=50)
    notes = models.TextField(default="Blank")


class BankLedger(models.Model):
    fiscal = models.ForeignKey(FiscalTerm, on_delete=models.CASCADE)
    budget = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, related_name='bank_budget_transactions')
    purpose = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, related_name='bank_purpose_transactions')
    transaction_id = models.UUIDField(default=uuid.uuid4)
    date = models.DateField(default=datetime.datetime.now)
    amount = models.FloatField(default=0.0)
    details = models.TextField(default="Blank")
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices, default=TransactionType.CREDIT)
    opening_balance = models.FloatField(default=0.0)
    closing_balance = models.FloatField(default=0.0)
    notes = models.TextField(default="Blank")


class VenmoLedger(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4)
    date = models.DateField(default=datetime.datetime.now)
    type = models.CharField(max_length=50, default="Payment")
    status = models.CharField(max_length=50, default="Complete")
    note = models.TextField(default="Blank")
    from_user = models.CharField(max_length=50, default="Blank")
    to_user = models.CharField(max_length=50, default="Blank")
    total_amount = models.FloatField(default=0.0)
    tip_amount = models.FloatField(default=0.0)
    tax_amount = models.FloatField(default=0.0)
    fee_amount = models.FloatField(default=0.0)
    net_amount = models.FloatField(default=0.0)
    tax_rate = models.FloatField(default=0.0)
    tax_exempt = models.BooleanField(default=False)
    budget = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, related_name='budget_venmo_ledgers')
    funding_source = models.CharField(max_length=50, default="Blank")
    funding_destination = models.CharField(max_length=50, default="Blank")
    purpose = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, related_name='purpose_venmo_ledgers')
    opening_balance = models.FloatField(default=0.0)
    closing_balance = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices, default=TransactionType.CREDIT)
    fiscal = models.ForeignKey(FiscalTerm, on_delete=models.CASCADE)


class MasterLedger(DBView):
    transaction_id = models.CharField(max_length=50)
    date = models.DateField(default=datetime.datetime.now)
    amount = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    budget = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)
    fiscal_term = models.CharField(max_length=50)
    fiscal_id = models.CharField(max_length=50)
    details = models.TextField(default=" ")

    view_definition = MASTER_LEDGER_VIEW

    class Meta:
        managed = False  # Managed must be set to False!
        db_table = 'master_ledger'
