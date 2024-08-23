from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, UpdateProfileView
urlpatterns = [
		path('register/', RegistrationView, name='register'),
		path('login/', LoginView, name='login'),
		path('logout/', LogoutView, name='logout'),
		path('profile/', UpdateProfileView, name='profile'),
]
