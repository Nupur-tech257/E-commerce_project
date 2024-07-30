from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddresss)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Profile)


