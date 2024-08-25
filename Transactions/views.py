from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TransactionForm, DepositForm, WithdrawForm, LoanRequestForm
from .constants import TRANSACTIONS_TYPE
from Transactions.models import Transaction

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

    
