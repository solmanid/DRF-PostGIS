from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request in SAFE_METHODS:
            return True
        else:
            return obj == request.user


class IsLoggedInUserOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
