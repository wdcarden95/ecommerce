from django.contrib import admin

# Register your models here.

# Imports models to be added
from .models import *

# Adds each object into admin panel
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
