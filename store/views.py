from django.shortcuts import render

# you can refer to models by simply ".models" because they're in the same directory
from .models import *

# Create your views here.

def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)

def cart(request):
	context = {}
	return render(request, 'store/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'store/checkout.html', context)