from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER, ACCOUNT_TYPE, DIVISION
from django.core.validators import MaxValueValidator, MinValueValidator, DecimalValidator

# Create your models here.


class Account(models.Model):
	user = models.OneToOneField(User, related_name='account' , on_delete=models.CASCADE)
	birth_date = models.DateField(verbose_name='Date of Birth',auto_now=False, auto_now_add=False)
	gender = models.CharField(verbose_name='Gender', choices=GENDER, max_length=50, default=None)
	account_type= models.CharField(verbose_name='Account Type', choices=ACCOUNT_TYPE, default=None, max_length=50)
	account_number=  models.IntegerField(verbose_name='Account Number',
		validators=[MaxValueValidator(5)]
	)
	balance =models.DecimalField(default=0, max_digits=12, decimal_places=2)
	initial_deposit_date = models.DateTimeField( auto_now_add=True)

class UserAddress(models.Model):
	user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
	division = models.CharField(verbose_name='Division', choices=DIVISION ,max_length=50, default=None)
	district = models.CharField(verbose_name='District', max_length=50)
	thana = models.CharField(verbose_name='Thana', max_length=50)
	post_code= models.CharField(verbose_name='Postal Code', max_length=50)