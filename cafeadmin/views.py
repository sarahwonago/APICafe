from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin
from cafecustomer.serializers import (
    CategorySerializer,
    FoodItemSerializer
)
from cafecustomer.models import (
    Category,
    FoodItem,
)


class AdminHome(APIView):
    """
    View for the admin dashboard.
    
    Only accessible to the admin.

    """


    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        """
        Handles GET request for the admin dashboard.
        
        Args:
            request (Request): The Http request

        Returns:
            response (Response): A response containing a welcome message.

        """

        message = {
            "detail": "welcome to the admin dashboard updated."
        }

        return Response(message, status=status.HTTP_200_OK)



class ListCreateCategory(APIView):
    """
    View to handle creating and listing categories.
    Allows searching for categories by name.

    Only accessible to admin users.

    Methods:
        get: List all categories or search for categories by name.
        post: Create a new category.

    """


    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CategorySerializer

    def get(self, request):
        """
        Handles GET request for fetching all categories
        or searching by category name.
        
        Args:
            request (Request): The Http request

        Returns:
            response (Response): A response containing all categories
            or search results.

        """

        search_query = request.query_params.get("name")

        if search_query:
            categories = Category.objects.filter(name__icontains=search_query)
        else:
            categories = Category.objects.all()

        if not categories.exists():
            response ={
                "detail":"No categories found."
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Handles POST request for  creating a new category.
        
        Args:
            request (Request): The Http request containing the data

        Returns:
            response (Response): A response containing the created category
            or the errors if it fails.

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


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def fooditem_create(request):
    """
    Creates a new fooditem.

    Only accessible to admin users.

    Args:
        request(Request): The HTTP request containing the fooditem data.

    Returns:
        Response: A JSON response containing the newly created fooditem or errors.
    """

    serializer = FoodItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_fooditems(request):
    """
    Fetches all fooditems under a category.

    Only accessible to admin users.

    Returns:
        Response: A JSON response containing all the fooditems under a category or errors.  
    """
    fooditems = FoodItem.objects.all()
    serializer = FoodItemSerializer(fooditems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def fooditem_detail(request, pk):
    """
    Retrieves, update or delete an existing fooditem.

    Only accessible to admin users.

    Args:
        pk (UUID): The UUID of the fooditem to retrieve, update or delete.

    Returns:
        Response: A JSON response confirming the deletion, updation, fetchingor errors.
    """

    try:
        fooditem = FoodItem.objects.get(pk=pk)

    except FoodItem.DoesNotExist:
        return Response({"detail": "Fooditem not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FoodItem(fooditem)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = FoodItem(fooditem, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fooditem.delete()
        return Response({"detail": "Food item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)