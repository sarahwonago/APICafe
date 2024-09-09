from django.urls import path
from .views import (AdminHome, ListCreateCategory, DetailUpdateDeleteCategory,
                    FoodItemCreateView, FoodItemListView
                    )

urlpatterns = [
    path("dashboard/", AdminHome.as_view(), name="admin-home"),
    path("categories/", ListCreateCategory.as_view(), name="category-list-create"),
    path("category/<uuid:pk>/", DetailUpdateDeleteCategory.as_view(), name="category-detail"),
    path("categories/<uuid:category_id>/addfooditem/", FoodItemCreateView.as_view(), name="create-fooditem"),
    path("categories/<uuid:category_id>/fooditems/", FoodItemListView.as_view(), name="list-fooditem"),
]