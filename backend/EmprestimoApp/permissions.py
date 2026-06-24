from rest_framework.permissions import BasePermission


class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    

class isNotAdmin(BasePermission):
    message = "Administradores não podem realizar esta operação."
    
    def has_permission(self, request, view):
        return not request.user.is_superuser