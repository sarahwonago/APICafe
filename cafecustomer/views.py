from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer
from django.shortcuts import get_object_or_404

from .models import (Cart, CartItem, Order, FoodItem)
from .serializers import (CartItemSerializer, )

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCustomer])
def customer_home(request):
    return Response({"detail":"Welcome to the customer dashboard"})


class AddToCartAPIView(APIView):
    """
    API view for adding a food item to the user's cart.

    The user must be authenticated, and the food item must exist in the system.
    If the food item is already in the cart, it will increase the quantity.

    Methods:
        post: Adds a fooditem to the cart.
    """

    permission_classes = [IsAuthenticated, IsCustomer]


    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to add a food item to the cart.
        The request must include the `fooditem` ID and `quantity`.
        """

        user = request.user
        fooditem_id = request.data.get("fooditem")
        quantity = request.data.get("quantity", 1) # default quantity is 1

        # validates that the fooditem exists
        fooditem = get_object_or_404(FoodItem, id=fooditem_id)

        # Gets or create a cart for the user
        cart, created = Cart.objects.get_or_create(user=user)

        # checks if the item already exists in the cart
        cart_item = CartItem.objects.filter(cart=cart, fooditem=fooditem).first()

        if cart_item:
            # if the item exists, update the quantity
            cart_item.quantity += int(quantity)
            cart_item.save()
        
        else:  
            # if the item does not exist, create an new CartItem 
            cartitem_data = {
                "cart":cart.id,
                "fooditem": fooditem.id,
                "quantity": quantity
            }

            # cartitem data passed to the serializer,it will be created in serializer create method
            serializer = CartItemSerializer(data=cartitem_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        cart_serializer = CartItemSerializer(cart_item)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
            

        



