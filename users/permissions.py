from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un superusuario.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
    

class IsCompany(BasePermission):
    """
    Permiso personalizado para verificar si el usuario es de tipo "Company".
    """
    def has_permission(self, request, view):
        # Verificar que el usuario esté autenticado y tenga un campo 'type' igual a "Company"
        user = request.user
        print(f"Usuario autenticado: {user}")
        if user.is_authenticated and hasattr(user, 'type') and user.type == "Company":
            return True
        return False