from rest_framework import permissions
from .models import UserProfile

class StaffPermission(permissions.BasePermission):
    """
    Custom permission to only allow staff members to access it.
    """

    def has_permission(self, request, view):
        return (not request.user.is_anonymous) and UserProfile.objects.filter(auth_user=request.user,user_type__in = ["Staff","Admin"]).exists()

class AdminPermission(permissions.BasePermission):
    """
    Custom permission to only allow admin members to access it.
    """

    def has_permission(self, request, view):
        return (not request.user.is_anonymous) and UserProfile.objects.filter(auth_user=request.user,user_type = "Admin").exists()