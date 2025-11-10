from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios editar un objeto.
    """
    def has_object_permission(self, request, view, obj):
        # Los permisos de lectura se permiten para cualquier solicitud
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Los permisos de escritura solo se permiten al propietario
        return obj.propietario == request.user


class IsPropietario(permissions.BasePermission):
    """
    Permiso que solo permite acceso a usuarios con rol de propietario.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'propietario'


class IsInquilino(permissions.BasePermission):
    """
    Permiso que solo permite acceso a usuarios con rol de inquilino.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'inquilino'


class IsAdminUser(permissions.BasePermission):
    """
    Permiso que solo permite acceso a usuarios administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'


class IsPropietarioOrInquilino(permissions.BasePermission):
    """
    Permiso que permite acceso a propietarios o inquilinos.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol in ['propietario', 'inquilino']