from django.urls import path
from .views import RegistrationView, LoginView

urlpatterns = [
		path('register/', RegistrationView, name='register'),
		path('login/', LoginView, name='login'),
]
