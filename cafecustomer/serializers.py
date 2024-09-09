from rest_framework import serializers
from .models import Category, FoodItem


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
        #image = models.ImageField(upload_to="food_images/", default="food_images/default.jpg")
        description (TextField): Brief description for the fooditem.
        created_at (DateTimeField): Timestamp when the fooditem was created.
        updated_at (DateTimeField): Timestamp when the fooditem was updated.
        is_available (BooleanField): Availability of the fooditem.
    """

    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = FoodItem
        fields = [
            "id", "name", "description", "price", "is_available", "created_at", "updated_at", "category"
        ]
        read_only_fields = ["id", "created_at"]