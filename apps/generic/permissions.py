from rest_framework.permissions import BasePermission

from apps.users.models import User


class IsAuthenticatedAndActive(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class IsNotGuest(IsAuthenticatedAndActive):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)
        return result and request.user.role != User.ROLE_GUEST


class IsReal(IsNotGuest):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)
        return result and request.user.is_real


class IsStaff(IsAuthenticatedAndActive):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)
        return result and request.user.is_staff


class IsModerator(IsAuthenticatedAndActive):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)
        return result and (request.user.is_superuser or request.user.role == User.ROLE_MODERATOR)
