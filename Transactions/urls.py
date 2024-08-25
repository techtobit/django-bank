from django.urls import path
from .views import DepositView, WithdrawView, LoanRequestView, ApproveLoanView
urlpatterns = [
		path('deposit/', DepositView, name='deposit'),
		path('withdraw/', WithdrawView, name='withdraw'),
		path('loan_request/', LoanRequestView, name='loan_request'),
		path('approve_loan/<int:loan_id>/', ApproveLoanView, name='approve_loan')
]
