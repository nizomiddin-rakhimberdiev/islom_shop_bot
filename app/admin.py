from django.contrib import admin
from .models import User, Product, Cart, Category, Order
# Register your models here.

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
