from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account, UserAddress
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

		def save(self, commit=True):
			fetch_user = super(UserCreationForm, self).save(commit=False)
			if commit == True:
				fetch_user.save()
				birth_date= self.cleaned_data.get("birth_date")
				gender= self.cleaned_data.get("gender")
				account_type= self.cleaned_data.get("account_type")
				division= self.cleaned_data.get("division")
				district= self.cleaned_data.get("district")
				thana= self.cleaned_data.get("thana")
				post_code= self.cleaned_data.get("post_code")

				Account.objects.create(
					user=fetch_user,
					birth_date = birth_date,
					gender = gender,
					account_type=account_type,
					account_number=1111+fetch_user.id
				)

				UserAddress.objects.create(
					user=fetch_user,
					division=division,
					district=district,
					thana=thana,
					post_code=post_code
				)

				return fetch_user


						
				