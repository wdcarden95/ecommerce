# For calling subroutines and functions on other pages such as cart total in the header.

import json
from .models import *

# Handle all the logic for guest user order
# Should see total of cart items on all views this function is used in.
def cookieCart(request):
    #Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('CART:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    # Loop through cart dictionary and add total quantity of each item
    # i is each item in the cart
    for i in cart:
        # Create empty cart for now for non-logged in user
		# Users without cart cookie will get error otherwise
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            cartItems += cart[i]['quantity']

            # Loop through cart, query items, and add up a total
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            # add on total and quantity to order dictionary in cart view's first "if" statement
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            # Create individual item for each i and then append that item to items[] list
            item = {
                'product':{
                    # Set 'id' equal to product.id, and so on for each attribute
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)

            # Checks if each item is digital or requires shipping
            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    # Add user data in store view
    # checks authenticated user
	if request.user.is_authenticated:
		customer = request.user.customer
		# either create an order or get order if it exists
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	# else if user is not authenticated
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

def guestOrder(request, data):
    print('User is not logged in...')

    print('COOKIES:', request.COOKIES)
    # Get cookieCart details
    name = data['form']['name']
    email = data['form']['email']
    cookieData = cookieCart(request)
    items = cookieData['items']

    # In case user decides to make an account, we want the same email address to have its purchase history
    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        # complete is False since this is an open cart until payment is conformed and processed
        complete=False,
        )

    # Loop through cart items and create order items by querying the product and setting the attributes.
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
