from django.contrib import admin
from .models import Book, Review, Cart, CartItem, Order

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)