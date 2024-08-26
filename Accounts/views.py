from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegistrationForm , UpdateProfileForm

def RegistrationView(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = RegistrationForm()
	return render(request, 'registration.html', {'form': form})


def LoginView(request):
	if request.method=='POST':
		username= request.POST['username']
		password= request.POST['password']
		user= authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			response= HttpResponse ('Not valid user id , password')
			return response
	return render(request, 'login.html')

def LogoutView(request):
	# if request.method=="POST":
		logout(request)
		return redirect('login')


def UpdateProfileView(request):
	if request.method=='POST':
		form =UpdateProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
	else:
		form = UpdateProfileForm(instance=request.user)
	return render(request, 'profile.html', {'form': form})


def PasswordChangeView(request):
	if request.method=='POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user.save()

			update_session_auth_hash(request, user)
			messages.success(request, 'You password was successfully updated')
		else:
			messages.error(request, 'Requset to update password failed')
	else:
		form=PasswordChangeForm(request.user)

	return render(request, 'password_change.html', {"form": form})
