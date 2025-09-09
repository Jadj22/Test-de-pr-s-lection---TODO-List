from .models import user_has_permission, user_has_role

def user_permissions(request):
    """
    Ajoute les méthodes de vérification des permissions au contexte des templates.
    """
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {}
        
    def has_perm(permission_codename):
        return user_has_permission(request.user, permission_codename)
        
    def has_role(role_name):
        return user_has_role(request.user, role_name)
    
    return {
        'has_perm': has_perm,
        'has_role': has_role,
        'is_admin': request.user.is_superuser or has_role('admin'),
    }
