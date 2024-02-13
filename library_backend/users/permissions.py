from rest_framework import permissions
from .models import UserProfile

class StaffPermission(permissions.BasePermission):
    """
    Custom permission to only allow staff members to access it.
    """

    def has_permission(self, request, view):
        return (request.user) and UserProfile.objects.filter(auth_user=request.user,user_type="Staff").exists()