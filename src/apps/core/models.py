import datetime

from django.db import models


# Create your models here.

class MasterLedger(models.Model):
    transaction_id = models.BigIntegerField(default=1)
    date = models.DateField(default=datetime.datetime.now)
    amount = models.FloatField(default=0)
    details = models.TextField(max_length=300, default="None")
    budget = models.TextField(default="Dues", max_length=100)
    purpose = models.TextField(default="Dues", max_length=100)
    account = models.TextField(default="Cash", max_length=100)
    transaction_type = models.TextField(default="credit")
