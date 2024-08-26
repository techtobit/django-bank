from django.urls import path
from .views import DepositView, WithdrawView, LoanRequestView, ApproveLoanView, TransactionReportView, TransferBalanceView
urlpatterns = [
		path('deposit/', DepositView, name='deposit'),
		path('withdraw/', WithdrawView, name='withdraw'),
		path('loan_request/', LoanRequestView, name='loan_request'),
		path('approve_loan/<int:loan_id>/', ApproveLoanView, name='approve_loan'),
		path('transaction_report', TransactionReportView, name='transaction_report'),
		path('transfer', TransferBalanceView, name='transfer')
]
