from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (AdminHome, ListCreateCategory, DetailUpdateDeleteCategory,
                    FoodItemCreateView, FoodItemListView, FoodItemDetailView,
                    DinningTableViewSet, SpecialOfferListCreateAPIView,SpecialOfferRetrieveUpdateDestroyAPIView,
                    FoodItemListAllView,
                    )

# defines the router and registers th viewset
router = DefaultRouter()
router.register("dinningtables", DinningTableViewSet, basename="dinningtable")

urlpatterns = [
    path("dashboard/", AdminHome.as_view(), name="admin-home"),
    path("categories/", ListCreateCategory.as_view(), name="category-list-create"),
    path("category/<uuid:pk>/", DetailUpdateDeleteCategory.as_view(), name="category-detail"),
    path("categories/<uuid:category_id>/addfooditem/", FoodItemCreateView.as_view(), name="create-fooditem"),
    path("categories/<uuid:category_id>/fooditems/", FoodItemListView.as_view(), name="list-fooditem"),
    path("fooditem/<uuid:fooditem_id>/", FoodItemDetailView.as_view(), name="fooditem-detail"),
    path("fooditems/", FoodItemListAllView.as_view(), name="fooditems"),
    path('specialoffers/', SpecialOfferListCreateAPIView.as_view(), name='specialoffer-list-create'),
    path('specialoffers/<uuid:offer_id>/', SpecialOfferRetrieveUpdateDestroyAPIView.as_view(), name='specialoffer-detail'),
]


urlpatterns += router.urls