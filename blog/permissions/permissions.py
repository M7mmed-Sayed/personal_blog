from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_authenticated and
                                 (request.user.is_staff or request.user == view.get_object().owner))