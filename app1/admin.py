from django.contrib import admin
from .models import CartItem,Product,Category,billing_address

admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(billing_address)
# /