from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def RegistrationView(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid:
			form = form.save()
			return redirect('')
	else:
		form = UserCreationForm()
	return render(request, 'registration.html', {'form': form})
		
