from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Разрешить только безопасные методы (GET) для чтения данных
            return True
        elif request.user.groups.filter(name='moderator').exists():
            # Запретить модераторам создавать и удалять курсы, разрешить остальные действия
            return False
        return True
