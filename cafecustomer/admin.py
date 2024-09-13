
from django.contrib import admin
from .models import (Category, FoodItem, DiningTable, Order, 
                     Cart, CartItem, Review, UserDinningTable, SpecialOffer, Transaction, 
                     CustomerPoint)

admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(DiningTable)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(UserDinningTable)
admin.site.register(CustomerPoint)
admin.site.register(SpecialOffer)
admin.site.register(Transaction)