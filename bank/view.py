from django.shortcuts import render
from django.http import HttpResponse

def Home(request):
	context= 'Page is rendering'
	return render(request, "index.html")