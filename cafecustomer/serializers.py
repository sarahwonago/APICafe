from rest_framework import serializers
from .models import (
    Category, FoodItem, DiningTable, SpecialOffer, CartItem, Cart, 
    Order, Notification, Review, RedemptionOption
    )


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Converts the Category model instances to JSON and vice versa.

    Fields:
        id (UUIDField): The unique identifier for the category.
        name (CharField): The name of the category.
        description (TextField): A brief description of the category.
        created_at (DateTimeField): The timestamp when the category was created.
        updated_at (DateTimeField): The timestamp when the category was last updated.
    """
    class Meta:
        model = Category
        fields = '__all__'
        

class FoodItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the FoodItem model.

    Converts the FoodItem model instances to JSON and vice versa.

    Fields:
        id (UUIDField): The unique identifier for the fooditem.
        category (ForeignKey): The category in which the fooditem belongs to.
        name (CharField): The name of the fooditem.
        price (DecimalField): The price of the fooditem.
        image (ImageField)
        description (TextField): Brief description for the fooditem.
        created_at (DateTimeField): Timestamp when the fooditem was created.
        updated_at (DateTimeField): Timestamp when the fooditem was updated.
        is_available (BooleanField): Availability of the fooditem.
    """

    category_id = serializers.UUIDField(required=False, write_only=True)
    category = CategorySerializer(read_only=True)
    image = serializers.ImageField(required = False)
    
    class Meta:
        model = FoodItem
        fields = [
            "id", "name", "description", "price","image", "is_available", "created_at", "updated_at", "category", "category_id"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

        def update(self, instance, validated_data):
            """
            Update a FoodItem instance.

            Args:
                instance (FoodItem): The existing food item instance to update.
                validated_data (dict): The validated data containing the updates.
            
            Returns:
                FoodItem: The updated food item instance.
            """
            category_id = validated_data.pop("category_id", None)

            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                    instance.category = category
                except Category.DoesNotExist:
                    raise serializers.ValidationError({"category_id":"Invalid Category Id provided."})
                
            # handles image update if provided 
            image = validated_data.pop("image", None)
            if image:
                instance.image = image
            
            return super().update(instance, validated_data)
        

class DinningTableSerializer(serializers.ModelSerializer):
    """
    Serializer for the dinningtable model.

    Converts the DinningTable model instance into JSON and vice versa.

    Fields:
        id (UUIDField): The unique identifier for the dinningtable
        table_number (PositiveIntegerField)- represents the table number
        is_occupied (BooleanField): Indicates whether the table is currently available.
        created_at (DateTimeField): Timestamp when the dinningtable was created.
        updated_at (DateTimeField): Timestamp when the dinningtable was updated.

    """

    class Meta:
        model= DiningTable
        fields = ["id","table_number", "is_occupied", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class SpecialOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for the SpecialOffer model.

    Fields:
        id (UUIDField): Unique identifier for the special offer.
        name (CharField): Name of the special offer.
        fooditem (FoodItem): The food item the offer applies to.
        discount_percentage (DecimalField): The percentage discount offered.
        start_date (DateTimeField): Start date of the offer.
        end_date (DateTimeField): End date of the offer.
        description (TextField): Additional details about the offer.
    """
    

    class Meta:
        model = SpecialOffer
        fields = ['id', 'name', 'fooditem','discount_percentage', 'start_date', 'end_date','is_active','description']

        
        
class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.

    Handles serialization and validation for adding items to the cart.

    Fields:
        id (UUIDField): Unique identifier for the order.
        cart(Cart): cart to store the cartitems.
        fooditem (FoodItem): the fooditem which represents the cartitem
        quantity (PositiveIntegerField): the cartitem quantity
        created_at (DateTimeField): Timestamp when the cartitem was created.
        price(DecimalField): the price for one fooditem
        total_price(DecimalField): the total price for the fooditem times the quantity
    """

    class Meta:
        model = CartItem
        fields = [
            "id", "cart", "fooditem", "quantity", "price", "total_price"
        ]

    def create(self, validated_data):
        """
        Create and return a new CartItem instance.
        Updates the cart's total price.
        """

        cart = validated_data.get("cart")
        fooditem = validated_data.get("fooditem")
        quantity = validated_data.get("quantity")

        # creates the cart item
        cartitem = CartItem.objects.create(
            cart=cart, fooditem=fooditem, quantity=quantity
        )

        # updates the carts total price
        cart.save()

        return cartitem
    
class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.

    Includes all cartitems.

    Fields:
        id (UUIDField): Unique identifier for the order.    
        user (User): the owner of the cart
        cartitems (CartItem): the cartitems
        total_price(DecimalField): the total price of the cart based on the items in it.
    """

    class Meta:
        model = Cart
        fields = [
            "id", "user", "cartitems", "total_price"
        ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Fields:
        id (UUIDField): Unique identifier for the order.
        user(User): the user to whom the order belongs to.
        order_items(CartItem): orderitems 
        total_price (DecimalField): the total price for the order
        is_paid (BooleanField): indicates if an order has been paid for.
        estimated_time (IntegerField): estimated delivery time for the order
        status (CharField): the order status
        created_at (DateTimeField): Timestamp when the order was created.
        updated_at (DateTimeField): Timestamp when the order was updated.
    """
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'is_paid', 'order_items', 'dining_table','estimated_time', 'status', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """
   Serialize for the Notifiction.

    Fields:
        id (UUIDField): Unique identifier for the notification.
        user(User): the user to whom the notification belongs.
        message(TextField): the body of the notification
        created_at (DateTimeField): Timestamp when the Notification was created.
       
    """

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Fields:
        id (UUIDField): Unique identifier for review.
        user(User): the reviewing the order.
        order(Order): the order being reviewed
        rating(PositiveIntegerField):the rating
        comment(TextField): the review text
        created_at (DateTimeField): Timestamp when the review was created.
    """

    class Meta:
        model = Review
        fields = ['id', 'user', 'order','rating','comment', 'created_at']
        read_only_fields = ['id', 'user', 'order', 'created_at']

class RedemptionOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the RedemptioOption model.

    Fields:
        foodItem(foodItem): the fooditem to be redeemed.
        points_required(PositiveIntegerField):points required to redeem this option
        description(TextField): the redemption option brief description
    """
    fooditem = FoodItemSerializer()

    class Meta:
        model = RedemptionOption
        fields = ['fooditem', 'points_required', 'description']
        