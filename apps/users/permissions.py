from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'Teachers'

class IsOwnerOrTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role.name == 'Teachers':
            return True
        return obj.student == request.user