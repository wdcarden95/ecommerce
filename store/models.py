from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	# Customer is One-to-One with User model. One customer per user.
	# on_delete removes the user if Customer is deleted
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)

	# Returns string name for each Customer
	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	# Boolean labels if product is digital or physical
	# default=False means by default items are Physical
	digital = models.BooleanField(default=False, null=True, blank=False)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	# part of Product
	# Prevents error when no image file is found to display for a product
	@property
	def imageURL(self):
		# product tries to look for its own image
		try:
			url = self.image.url
		# if the try doesn't work, render an empty string
		except:
			url = ''
		return url

class Order(models.Model):
	# Order has Many-To-One relationship with customers. customer can have multiple orders.
	# on_delete=Models.SET NULL If customer gets deleted, set customer to null, don't delete the order.
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	# if complete is false, it is an open cart and can add more items.
	# If True, it is a closed cart and items added to go new order.
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	# Dynamically displays cart order total price
	@property
	def get_cart_total(self):
		# gets all order items
		orderitems = self.orderitem_set.all()
		# runs a loop to go through each order item and add up a total
		total = sum([item.get_total for item in orderitems])
		return total

	# Dynamically displays total number of cart items
	@property
	def get_cart_items(self):
		# gets all order items
		orderitems = self.orderitem_set.all()
		# runs a loop to go through each order item and add up a total
		total = sum([item.quantity for item in orderitems])
		return total

# OrderItem is an item within our cart; Many-To-One relationship: Cart can have multiple OrderItems
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	# A single order can have multiple orderitems
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	# Dynamically sets totals for items in cart
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	# Attatch shipping address to customer and order.
	# If an order gets deleted, still have a shipping address for a customer.
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	zipcode = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
