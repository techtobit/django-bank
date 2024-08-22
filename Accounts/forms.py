from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .constants import DIVISION, GENDER, ACCOUNT_TYPE

class RegistrationForm(UserCreationForm):

		birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
		gender = forms.ChoiceField( choices=GENDER, required=True)
		account_type = forms.ChoiceField( choices=ACCOUNT_TYPE, required=True)
		division = forms.ChoiceField( choices=DIVISION, required=True)
		district = forms.CharField(required=True)
		thana = forms.CharField(required=True)
		post_code = forms.CharField(required=True)
		class Meta:
				model = User
				fields = ['username', 'first_name', 'last_name','email', 'birth_date', 'gender', 'account_type',
				'division', 'district', 'thana', 'post_code', 'password1', 'password2',]