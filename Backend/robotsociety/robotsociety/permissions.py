from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # We want to check is_admin instead of is_staff
        return bool(request.user and request.user.is_admin)