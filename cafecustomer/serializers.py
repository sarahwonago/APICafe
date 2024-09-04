from rest_framework import serializers
from .models import Category


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
        