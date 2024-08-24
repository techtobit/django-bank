from django.db import models
from Accounts.models import Account
from .constants import TRANSACTIONS_TYPE

# Create your models here.
class Transactions(models.Model):
	account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)

	transaction_type= models.CharField(choices=TRANSACTIONS_TYPE, null=True, max_length=12)
	balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
	timestamp= models.DateTimeField(auto_now_add=True)
	loan_approv= models.BooleanField(default=False)