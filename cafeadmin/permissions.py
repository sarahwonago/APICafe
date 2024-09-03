from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    # the message displayed if the is_admin role does not pass
    message = "You must be a an admin to access this resource."

    def has_permission(self, request, view):
        return request.user.role == 'admin'