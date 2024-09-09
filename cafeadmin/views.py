from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

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

class DetailUpdateDeleteCategory(APIView):
    """
    View to handle retrieving, updating, and deleting a single category.

    Only accessible to admin users.

    Methods:
        get: Retrieve a single category by its ID.
        put: Update a category.
        delete: Delete a category.
    """


    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CategorySerializer

    def get_object(self, pk):
        """
        Utility function for fetching a single category by ID.

        Args:
            pk (UUID): The primary key of the category to retrieve.

        Returns:
            category (Category): The fetched category.
        """

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            category = None
        
        return category

    def get(self, request, pk=None):
        """
        Handle GET requests for retrieving a single category by ID.

        Args:
            pk (UUID): The primary key of the category to retrieve.
            request (Request): The Http request

        Returns:
            Response: A response containing the category data.
        """
        
        category = self.get_object(pk=pk)

        if not category:
            response = {
                "detail": "Category not found."
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        """
        Handle PUT requests for updating an existing category by ID.

        Args:
            pk (UUID): The primary key of the category to update.
            request (Request): The Http request

        Returns:
            Response: A response containing the updated category data or validation errors.
        """

        data = request.data

        category = self.get_object(pk=pk)

        if not category:
            response = {
                "detail": "Category not found."
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(data=data, instance=category)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        """
        Handle DELETE requests for deleting a category by ID.

        Args:
            pk (UUID): The primary key of the category to delete.
            request (Request): The Http request

        Returns:
            Response: A response confirming deletion.
        """
        category = self.get_object(pk=pk)

        if not category:
            response = {
                "detail": "Category not found."
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()

        response = {
            "detail":"category deleted successfully"
        }
       
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    

class FoodItemCreateView(APIView):
    """
    View to handle creating of fooditems under a specific category.

    Only accessible to admin users.

    Methods:
        
        post: Create a new fooditem under the specified category.

    """


    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = FoodItemSerializer

    def post(self, request, category_id):
        """
        Handle POST request to create a new food item under the specified category.

        Args:
            request (HttpRequest): The HTTP request object containing the food item data.
            category_id (UUID): The UUID of the category under which the food item is created.

        Returns:
            Response: A JSON response with the created food item data or an error message.
        """

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")
        
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            # Set the category field to the retrieved category
            serializer.save(category=category)
            # Return the created food item data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodItemListView(APIView):
    """
    View to handle listing of fooditems under a specific category.

    Only accessible to admin users.

    Methods:
        
        get: Create a new fooditem under the specified category.

    """


    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = FoodItemSerializer

    def get(self, request, category_id):
        """
        Handle get request to fetch fooditems under the specified category.

        Args:
            request (HttpRequest): The HTTP request.
            category_id (UUID): The UUID of the category for the fooditems.

        Returns:
            Response: A JSON response with all the fooditems or an error message.
        """

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")
        
        fooditems = FoodItem.objects.filter(category=category)

        if not fooditems:
            return Response({"detail":"No fooditems under this category"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FoodItemSerializer(fooditems, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FoodItemDetailView(APIView):
    """
    View to handle retrieving, updating or deleting of a single fooditem.

    Only accessible to admin users.

    Methods:
        
        get: fetches a fooditem.
        put: updates a fooditem.
        delete: deletes a fooditem.

    """


    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = FoodItemSerializer

    def get_object(self, fooditem_id):
        """
        Utility function to fetch a fooditem.

        Args:
            fooditem_id (UUID): UUID of the fooditem to be fetched.
        Returns:
            fooditem (FoodItem): fooditem or error if not found.
        """

        try:
            fooditem = FoodItem.objects.get(id=fooditem_id)

        except FoodItem.DoesNotExist:
            return Response({"detail": "FoodItem not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return fooditem
    
    def get(self, request, fooditem_id):
        """
        Handle GET requests to retrieve a specific food item by its ID.
        
        Args:
            request (Request): The HTTP request object.
            fooditem_id (UUID): The ID of the food item to retrieve.
        
        Returns:
            A JSON response containing the food item details.
        """
        fooditem = self.get_object(fooditem_id=fooditem_id)

        serializer = FoodItemSerializer(fooditem)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, fooditem_id):
        """
        Handle PUT requests to update a specific food item by its ID.
        
        Args:
            request (Request): The HTTP request object.
            fooditem_id (UUID): The ID of the food item to update.
        
        Returns:
            A JSON response containing the updated food item details.
        """
        fooditem = self.get_object(fooditem_id=fooditem_id)

        serializer = FoodItemSerializer(data=request.data, instance=fooditem)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fooditem_id):
        """
        Handle DELETE requests to delete a specific food item by its ID.
        
        Args:
            request (Request): The HTTP request object.
            fooditem_id (UUID): The ID of the food item to delete.
        
        Returns:
            A JSON response confirming the deletion.
        """
        fooditem = self.get_object(fooditem_id=fooditem_id)
        fooditem.delete()

        return Response({"detail":"Fooditem deleted successfully."}, status=status.HTTP_200_OK)
