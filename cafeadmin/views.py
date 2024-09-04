from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin
from cafecustomer.serializers import (
    CategorySerializer,
)
from cafecustomer.models import (
    Category,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def admin_home(request):
    return Response({"detail":"Welcome to the admin dashboard"})

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def add_category(request):
    """
    Create a new category.

    Only accessible to admin users.

    Args:
        request (Request): The HTTP request containing the category data.

    Returns:
        Response: A JSON response containing the newly created category or errors.
    """
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_categories(request):
    """
    Retrieve a list of all categories.

    Only accessible to admin users.

    Returns:
        Response: A JSON response containing a list of all categories.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdmin])
def update_category(request, pk):
    """
    Update an existing category by its UUID.

    Only accessible to admin users.

    Args:
        request (Request): The HTTP request containing the updated category data.
        pk (UUID): The UUID of the category to update.

    Returns:
        Response: A JSON response containing the updated category or errors.
    """
    try:
        category = Category.objects.get(pk=pk)

    except Category.DoesNotExist:
        ct = {
            "detail": "Category not found."
        }
        return Response(ct, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def delete_category(request, pk):
    """
    Delete an existing category by its UUID.

    Only accessible to admin users.

    Args:
        pk (UUID): The UUID of the category to delete.

    Returns:
        Response: A JSON response confirming the deletion.
    """

    try:
        category = Category.objects.get(pk=pk)

    except Category.DoesNotExist:
        ct = {
            "detail": "Category not found."
        }
        return Response(ct, status=status.HTTP_404_NOT_FOUND)
    
    category.delete()

    return Response({"detail":"Category deleted successfully."},status=status.HTTP_204_NO_CONTENT)