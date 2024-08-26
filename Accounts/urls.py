from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, UpdateProfileView, PasswordChangeView
urlpatterns = [
		path('register/', RegistrationView, name='register'),
		path('login/', LoginView, name='login'),
		path('logout/', LogoutView, name='logout'),
		path('profile/', UpdateProfileView, name='profile'),
		path('password_change/', PasswordChangeView, name='password_change'),
]
