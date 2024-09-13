from rest_framework import serializers
from .models import (Category, FoodItem, DiningTable)


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
