"""
Custom permissions for BlockHire API.
"""
from rest_framework.permissions import BasePermission


class AllowAnyPermission(BasePermission):
    """
    Allow any request - no authentication required.
    """
    def has_permission(self, request, view):
        return True
