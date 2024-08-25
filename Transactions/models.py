from django.db import models
from django import forms
from Accounts.models import Account
from .constants import TRANSACTIONS_TYPE

# Create your models here.
class Transaction(models.Model):
	account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)

	amount= amount = models.DecimalField(max_digits=12, decimal_places=2)
	transaction_type= models.CharField(choices=TRANSACTIONS_TYPE, null=True, max_length=12)
	balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
	timestamp= models.DateTimeField(auto_now_add=True)
	loan_approv= models.BooleanField(default=False)

	