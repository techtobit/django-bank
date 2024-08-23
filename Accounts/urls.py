from django.urls import path
from .views import RegistrationView, LoginView, LogoutView

urlpatterns = [
		path('register/', RegistrationView, name='register'),
		path('login/', LoginView, name='login'),
		path('logout/', LogoutView, name='logout'),
]
