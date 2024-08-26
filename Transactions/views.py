from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime  
from decimal import Decimal
from django.db.models import Sum
from .forms import TransactionForm, DepositForm, WithdrawForm, LoanRequestForm, TransferBalanceFrom
from .constants import TRANSACTIONS_TYPE
from Transactions.models import Transaction
from Accounts.models import Account

def TransactionView(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, account=request.user.account)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = TransactionForm(account=request.user.account)
    
    return render(request, 'transaction_form.html', {'form': form})

@login_required
def DepositView(request):
    account=request.user.account
    form=DepositForm(request.POST or None, account=account)
    if form.is_valid():
        transaction=form.save(commit=False)
        transaction.account=account
        transaction.transaction_type='deposit'
        transaction.balance_after_transaction= account.balance+transaction.amount
        account.balance+=transaction.balance_after_transaction
        account.save()
        transaction.save()
        return redirect(reverse_lazy('home'))
    return render(request, 'transaction_form.html', {'form': form,  'title':'Deposit Money'})


@login_required
def WithdrawView(request):
    account = request.user.account 
    form = WithdrawForm(request.POST or None, account=account)
    
    if request.method == 'POST':
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = 'withdraw'
            transaction.balance_after_transaction = account.balance - transaction.amount
            account.balance = transaction.balance_after_transaction
            account.save()
            transaction.save()
            return redirect('withdraw')
    
    return render(request, 'transaction_form.html', {'form': form, 'title':'Withdraw Money'})

@login_required
def LoanRequestView(request):
    account=request.user.account
    form=LoanRequestForm(request.POST or None, account=account)
    if request.method=="POST":
        if form.is_valid():
            current_loan_count=Transaction.objects.filter(
                account=account, transaction_type='loan', loan_approv=True).count()
            if current_loan_count>3:
                return HttpResponse('You crossed the loan limit')
            
            transaction=form.save(commit=False)
            transaction.account=account
            transaction.transaction_type='loan'
            transaction.balance_after_transaction=account.balance
            # transaction.loan_approv=True
            transaction.save()

            amount=form.cleaned_data.get('amount')
            messages.success(
                request,
                f'Loan request for {"{:,.2f}".format(float(amount))}$ submited succesfull'
            )
            return redirect('loan_request')
    loan_list=Transaction.objects.filter(account=account, transaction_type='loan')
    return render(request, 'transaction_form.html', {'form': form, 'loan_list':loan_list, 'title':'Loan Request'})

@login_required
def ApproveLoanView(request, loan_id):
    account=request.user.account
    # loan=Transaction.objects.filter(account=account, id=loan_id, transaction_type='loan')
    loan = get_object_or_404(Transaction, id=loan_id, transaction_type='loan')

    if not loan.loan_approv:
        loan.loan_approv = True
        loan.save()
        messages.success(request, 'Loan request approved successfully!')
    else:
        messages.info(request, 'This loan has already been approved.')
    return redirect('loan_request')


def TransactionReportView(request):
    account=request.user.account
    transactions= Transaction.objects.filter(account=account)

    balance=0
    start_date_str=request.GET.get('start_date')
    end_date_str=request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date_str=datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date_str=datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
        transactions = transactions.filter(
            timestamp__date__gte=start_date_str,
            timestamp__date__lte=end_date_str
        )
        
        balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
    else:
        balance=account.balance

    context={
        'transactions': transactions.distinct(),
        'account': account,
        'balance': balance
    }

    return render(request, 'transaction_report.html', context)



# def TransferBalanceView(request):
#     sender_account=request.user.account
#     if request.method=='POST':
#         form=TransferBalanceFrom(request.POST, sender_account=sender_account)
#         if form.is_valid():
#             recipient_account_number=form.cleaned_data['recipient_account_number']
#             amount=form.cleaned_data['recipient_account_number']

#             recipient_account=Account.objects.filter(account_number=recipient_account_number)

#             sender_account.balance -=amount
#             sender_account.save()

#             recipient_account.balance +=amount
#             recipient_account.save()

#             Transaction.objects.create(
#                 account=sender_account.id,
#                 amount= amount,
#                 transaction_type='transfer',
#                 balance_after_transaction =sender_account.balance
#             )

#             Transaction.objects.create(
#                 account=recipient_account.id,
#                 amount= amount,
#                 transaction_type='deposit',
#                 balance_after_transaction =recipient_account.balance
#             )

#             messages.success(request, 'Amount Transfer Succesfull')
#             return redirect('transfer')
#     else:
#         form=TransferBalanceFrom()
    
#     context={
#         'form':form,
#         'title': 'Transfer Money'
#     }

#     return render(request, 'transfer.html', context)



def TransferBalanceView(request):
    if request.method == 'POST':
        form=TransferBalanceFrom(request.POST)
        if form.is_valid():
            recipient_account_number = form.cleaned_data['recipient_account_number']
            amount = form.cleaned_data['amount']
            
        
        try:
            recipient_account = get_object_or_404(Account, account_number=recipient_account_number)
        except Http404:
            messages.error(request, "Recipient account not found.")
            return redirect('transfer')

        sender_account = request.user.account
        
        # Ensure sufficient balance
        if sender_account.balance < amount:
            messages.error(request, "Insufficient balance for this transfer.")
            return redirect('transfer')

        # Proceed with the transfer
        sender_account.balance -= amount
        recipient_account.balance += amount
        sender_account.save()
        recipient_account.save()

        # Record the transaction for the sender
        Transaction.objects.create(
            account=sender_account,
            amount=amount,
            transaction_type='transfer_out',  # or 'debit' or any other suitable label
            balance_after_transaction=sender_account.balance,
        )

        # Record the transaction for the recipient
        Transaction.objects.create(
            account=recipient_account,
            amount=amount,
            transaction_type='transfer_in',  # or 'credit' or any other suitable label
            balance_after_transaction=recipient_account.balance,
        )

        messages.success(request, f"Successfully transferred {amount} to account {recipient_account_number}.")
        return redirect('transfer')  # Redirect to a success page or any other appropriate page
    else:
        form=TransferBalanceFrom()
    return render(request, 'transfer.html', {'form':form})
