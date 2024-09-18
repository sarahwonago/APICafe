from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer
from django.shortcuts import get_object_or_404

from .models import (Cart, CartItem, Order, FoodItem, DiningTable,
                     Notification)
from .serializers import (CartItemSerializer, CartSerializer, OrderSerializer,
                          NotificationSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCustomer])
def customer_home(request):
    return Response({"detail":"Welcome to the customer dashboard"})


class AddToCartAPIView(APIView):
    """
    API view for adding a food item to the user's cart.

    The user must be authenticated, and the food item must exist in the system.

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
            # if the item exists, item already exists in cart
            return Response({"detail":"Item already exists in cart"}, status=status.HTTP_200_OK)
        
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
            
       
class CartItemsAPIView(APIView):
    """
    API view for fetching all the cartitems.

    The user must be authenticated to view the cart.

    Methods:
        get: fetches all cartitems in the user's cart.
    """

    permission_classes = [IsAuthenticated, IsCustomer] 


    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve all cart items for the authenticated user.
        """
        user = request.user

        # fetches or creates a cart for the user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = cart.cartitems.all()

        if cart_items:
            serializer = CartItemSerializer(cart_items, many=True)
            response = {
                "cartitems": serializer.data,
                "total_price":cart.total_price
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({"detail":"Cart is empty."}, status=status.HTTP_200_OK)
    
class CartItemUpdateAPIView(APIView):
    """
    API view for updating the cartitem.

    The user must be authenticated to view the cart.

    Methods:
        patch: updates the quantity for a specific cartitem.
        delete: deletes a specific cartitem from the cart.
    """

    permission_classes = [IsAuthenticated, IsCustomer] 

    def patch(self, request, *args,  **kwargs):
        """
        Handle PATCH requests to update a cartitem's quantity.

        The request must include the quantity field.
        """
        user = request.user

        cartitem_id = kwargs.get("cartitem_id") # passed in the url
        quantity = request.data.get("quantity")

        # validates the cartitem belongs to the user
        cartitem = get_object_or_404(CartItem, id=cartitem_id, cart__user=user)

        # updates the quantity if provided:
        if quantity and int(quantity) > 0:
            cartitem.quantity = int(quantity)
            cartitem.save()
        else:
          return Response({"detail":"Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args,  **kwargs):
        """
        Handle DELETE requests to remove a cartitem from the user's cart.

        """
        user = request.user

        cartitem_id = kwargs.get("cartitem_id")

        # validates the cartitem belongs to the user
        cartitem = get_object_or_404(CartItem, id=cartitem_id, cart__user=user)

        # deletes the cartitem
        cartitem.delete()

        return Response({"detail":"Item removed from Cart"}, status=status.HTTP_200_OK)
    

class CreateOrderAPIView(APIView):
    """
    API view for creating an order from the cart.
    Orders will only be created if there are cart items in the cart.

    The user must be authenticated to create an order.

    Methods:
        post: creates a new order.
    """

    permission_classes = [IsAuthenticated, IsCustomer] 

    def post(self, request, *args, **kwargs):
        """
        Handles post requests to create an order from the user's cart.
        - Ensures that the cart is not empty.
        - Fetches the total price from the cart.
        - Clears the cart once the order has been created.

        Returns:
        - A success message with the created order details and totalprice
        - A message if the cart is empty.
        """


        user = request.user
        # fetches the dinning table 
        dinning_table_id = request.data.get("dining_table")

        try:
            dinning_table = DiningTable.objects.get(id=dinning_table_id)
        except DiningTable.DoesNotExist:
            return Response({"detail":"Please indicate the dinning table."}, status=status.HTTP_400_BAD_REQUEST)


        cart, created = Cart.objects.get_or_create(user=user)
        cartitems = cart.cartitems.all()

        # if cart is empty
        if not cartitems.exists():
            response = {
                "message": "Your cart is empty. Please add items to cart before placing an order"
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # gets the total price from the cart
        total_price = cart.total_price

        # creates a new order
        order = Order.objects.create(
            user = user,
            total_price = total_price,
            dining_table= dinning_table
        )

        # add the cart items to the order
        # order.order_items.add(cartitems)
        # order.save()

        # cleares the cart after creating the order
        cartitems.delete()

        serializer = OrderSerializer(order)

        response = {
            "message": "Order created successfully",
            "order": serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class PaymentAPIView(APIView):
    """
    API view for handling payment after an order has been created.

    The user must be authenticated.

    Methods:
        post: handle post requests for making payments.
    """

    permission_classes = [IsAuthenticated, IsCustomer] 

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for processing payments.
        - The user will provide payment information.
        - Once the payment is successful, the order will be updated, and the user will receive a notification.

        Returns:
            - A success message if payment is processed successfully.
            - An error message if something goes wrong.
        """
        
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.is_paid:
            return Response(
                {
                "message":"The order has already been paid."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # if order is not paid for, payment processing goes here
        # implement daraja api

        # simulate payment is paid for now
        payment_successful = True

        if payment_successful:
            order.is_paid = True
            order.save()

            # send a payment notification to the cafeadmin


            # sends an in app notification to  the customer
            notification = Notification.objects.create(
                user = request.user,
                message = f"Your payment for Order {order.id} has been processed sucessfully"
            )

            notification_serializer = NotificationSerializer(notification)

            return Response(
                {
                    "message": "Payment processed successfully.",
                    "order": OrderSerializer(order).data,
                    "notification": notification_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Payment failed. Please try again."},
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderHistoryAPIView(APIView):
    """
    API view for fetching the order history.

    The user must be authenticated.

    Methods:
        get: retrieves all past orders for the user.
    """

    permission_classes = [IsAuthenticated, IsCustomer] 

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve all past orders for the authenticated user.

        Returns:
            - A list of the user's past orders.
        """

        orders = Order.objects.filter(user=request.user)

        if orders:
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message":"You have no past orders."}, status=status.HTTP_200_OK)

