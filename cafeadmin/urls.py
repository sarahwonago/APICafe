from django.urls import path
from .views import (AdminHome, ListCreateCategory, update_category, get_categories,delete_category,
                    fooditem_create, get_fooditems, fooditem_detail
                    )

urlpatterns = [
    path("dashboard/", AdminHome.as_view(), name="admin-home"),
    path("categories/list/", ListCreateCategory.as_view(), name="list_create_category"),
    path("categories/", get_categories, name="get_categories"),
    path("categories/update/<uuid:pk>/", update_category, name="update_category"),
    path("categories/delete/<uuid:pk>/", delete_category, name="delete_category"),
    path("categories/fooditem/create/", fooditem_create, name="create_fooditem"),
    path("categories/fooditems/", get_fooditems, name="get_fooditems"),
    path("categories/fooditem/detail/<uuid:pk>/", fooditem_detail, name="detail_fooditem"),
]