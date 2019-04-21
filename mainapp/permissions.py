from rest_framework import permissions


class IsOwnerOfReservation(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user.pk == request.user.pk
