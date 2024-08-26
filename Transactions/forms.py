from django import forms
from decimal import Decimal
from .models import Transaction
from Accounts.models import Account
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
    

# class TransferBalanceFrom(forms.Form):
#     recipient_account_number= forms.IntegerField(label="Recipient's Account Number", required=True)
#     amount= forms.DecimalField(max_digits=12, decimal_places=2, required=True)

#     def __init__(self, *args, **kwargs):
#         sender_account_number= kwargs.pop('sender_account', None)
#         super().__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = super().clean()
#         recipient_account_number = cleaned_data.get('recipient_account_number')
#         amount=cleaned_data.get('amount')
            
#         try:
#             recipient_account=Transaction.objects.filter(account_number=recipient_account_number)
#         except Account.DoesNotExist:
#             raise forms.ValidationError('The recipient account does not exit.')

#         if self.sender_account_number.balance < amount:
#             raise forms.ValidationError("Insufficient balance for this transaction.")
        
#         return cleaned_data



class TransferBalanceFrom(forms.Form):
    recipient_account_number= forms.IntegerField(
        label="Recipient's Account Number", 
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter recipient account number'
        })
        )
    amount= forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        required=True, 
        label="Recipient's Account Number", 
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to ransfer'
        })
    )
