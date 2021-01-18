from django.shortcuts import render

# you can refer to models by simply ".models" because they're in the same directory
from .models import *

# imported to allow the response to updateItem to be a JsonResponse
from django.http import JsonResponse

# Used in updateItem view to parse data
import json

import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
	# Call cartData from utils.py to display cart item count on page
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	# Query cart item count
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
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

	# Query the customer and create the order
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	# Create order item
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	# Add 1 or subtract 1 from quantity
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	# if quantity passes 0, remove item from cart
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

# Send back payment complete response when payment completes
def processOrder(request):
	# Create transaction id out of datetime
	transaction_id = datetime.datetime.now().timestamp()
	# get data
	data = json.loads(request.body)

	if request.user.is_authenticated:
		# get customer
		customer = request.user.customer
		# get order
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guestOrder(request, data)

	# get total
	total = float(data['form']['total'])
	# set order transaction id
	order.transaction_id = transaction_id

	# confirm total
	if total == order.get_cart_total:
		order.complete = True
	order.save()

	# if items are being shipped, create shipping address object
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment complete!', safe=False)
