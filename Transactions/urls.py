from django.urls import path
from .views import DepositView, WithdrawView
urlpatterns = [
		path('deposit/', DepositView, name='deposit'),
		path('withdraw/', WithdrawView, name='withdraw')
]
