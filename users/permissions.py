from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """ Функция выборки модераторов """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(BasePermission):
    """ Функция выборки владельцев """
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsTeacher(BasePermission):
    """ Функция выборки преподавателей """
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Teachers").exists()
