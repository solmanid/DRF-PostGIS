from rest_framework.permissions import BasePermission


class IsSupervisorUser(BasePermission):
    """
    Allows access only to Supervisor users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_supervisor)
