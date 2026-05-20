from rest_framework import permissions


class IsOwnerAndDraftOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.reporter == request.user
            and obj.status == 'DRAFT'
        )