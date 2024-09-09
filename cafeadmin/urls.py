from django.urls import path
from .views import (AdminHome, ListCreateCategory, DetailUpdateDeleteCategory,
                    )

urlpatterns = [
    path("dashboard/", AdminHome.as_view(), name="admin-home"),
    path("categories/", ListCreateCategory.as_view(), name="category-list-create"),
    path("category/<uuid:pk>/", DetailUpdateDeleteCategory.as_view(), name="category-detail"),
]