from django.urls import path
from .views import (admin_home, add_category, update_category, get_categories,delete_category
                    )

urlpatterns = [
    path("dashboard/", admin_home, name="admin-home"),
    path("categories/create/", add_category, name="create_category"),
    path("categories/", get_categories, name="get_categories"),
    path("categories/update/<uuid:pk>/", update_category, name="update_category"),
    path("categories/delete/<uuid:pk>/", delete_category, name="delete_category"),
]