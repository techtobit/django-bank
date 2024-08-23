from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import RegistrationForm

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
