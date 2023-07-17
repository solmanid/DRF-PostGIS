from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request in SAFE_METHODS:
            return True
        else:
            return obj.user == request.user
