from rest_framework import permissions


class IsOwnerDraftOrAdminStatusOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            return True

        if user.is_admin:
            return True

        return (
            obj.reporter == user
            and obj.status == 'DRAFT'
        )