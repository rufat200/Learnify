from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'owner', None)

        if hasattr(obj, 'student'):
            owner = obj.student
        elif hasattr(obj, 'course'):
            owner = getattr(obj.course, 'owner', None)
        elif hasattr(obj, 'lesson'):
            owner = getattr(obj.lesson.course, 'owner', None)

        return owner == request.user or request.user.is_superuser
