from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TransactionForm, DepositForm, WithdrawForm
from .constants import TRANSACTIONS_TYPE

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