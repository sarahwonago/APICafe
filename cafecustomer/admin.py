
from django.contrib import admin
from .models import (Category, FoodItem, DiningTable, Order, 
                     OrderItem, Review,UserDinningTable, SpecialOffer, Transaction, 
                     CustomerPoint)

admin.site.register(Category)
admin.site.register(FoodItem)
admin.site.register(DiningTable)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(UserDinningTable)
admin.site.register(CustomerPoint)
admin.site.register(SpecialOffer)
admin.site.register(Transaction)