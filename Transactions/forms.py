from django import forms
from decimal import Decimal
from .models import Transaction
from .constants import TRANSACTIONS_TYPE

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.user_account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)

class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You need to deposit at least ${min_deposit_amount}')
        return amount

class WithdrawForm(TransactionForm):
    def clean_amount(self):
        min_withdraw_amount = 10
        max_withdraw_amount = 50000
        balance = self.user_account.balance if self.user_account else None
        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(f'The minimum withdrawal amount is ${min_withdraw_amount}.')

        if balance < amount:
            raise forms.ValidationError('Insufficient Balance. Your account balance is too low.')
        
        if amount > max_withdraw_amount:
            raise forms.ValidationError(f'The maximum withdrawal amount is ${max_withdraw_amount}.')
        

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        balance=self.user_account.balance if self.user_account else None
        max_eligible_loan= balance*2
        amount = self.cleaned_data.get('amount')
        if max_eligible_loan < amount:
            raise forms.ValidationError(f'You are eligible loan in between {max_eligible_loan}')
        
        return amount
    


