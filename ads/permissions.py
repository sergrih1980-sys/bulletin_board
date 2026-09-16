from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Владелец может редактировать; остальные — только чтение."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    """Админ может всё; остальные — только чтение."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAdminOrOwner(BasePermission):
    """Админ или владелец — может; остальные — нет."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.author == request.user


class IsAuthenticatedOrListOnly(BasePermission):
    """Аноним видит только список; детали — только авторизованным."""
    def has_permission(self, request, view):
        if request.method == "GET" and view.action == "list":
            return True
        return request.user and request.user.is_authenticated



