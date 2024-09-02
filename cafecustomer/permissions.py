from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    message = "You must be a customer to access this resource."
    
    def has_permission(self, request, view):
        return request.user.role == 'customer'