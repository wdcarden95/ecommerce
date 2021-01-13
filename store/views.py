from django.shortcuts import render

# you can refer to models by simply ".models" because they're in the same directory
from .models import *

# imported to allow the response to updateItem to be a JsonResponse
from django.http import JsonResponse

# Used in updateItem view to parse data
import json

# Create your views here.

def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)

def cart(request):
	# checks authenticated user
	if request.user.is_authenticated:
		customer = request.user.customer
		# either create an order or get order if it exists
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	# else if user is not authenticated
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		# either create an order or get order if it exists
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	# else if user is not authenticated
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {'items':items, 'order':order}
	return render(request, 'store/checkout.html', context)

# This view processes the action of a user clicking "add to cart" when it receives the data
def updateItem(request):
	# send POST request
	data = json.loads(request.body)
	# get cart ID sent from cart.js
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)
	return JsonResponse('Item was added', safe=False)
