from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Кастомный пермишен, позволяющий доступ к объекту только его владельцу.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
