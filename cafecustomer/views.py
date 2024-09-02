from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCustomer])
def customer_home(request):
    return Response({"detail":"Welcome to the customer dashboard"})
