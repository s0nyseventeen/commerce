from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	return render(request, 'accounts/homepage.html')


def profile(request):
	return render(request, 'accounts/profile.html')


def customer(request):
	return render(request, 'accounts/customer.html')