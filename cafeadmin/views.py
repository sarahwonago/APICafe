from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def admin_home(request):
    return Response({"detail":"Welcome to the admin dashboard"})
