from functools import wraps
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .models import user_has_permission


def require_permission(permission_codename, login_url=None, message=None, json_response=False):
    """
    Décorateur pour vérifier si un utilisateur a une permission spécifique.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if json_response:
                    return JsonResponse(
                        {'error': 'Authentication required'}, 
                        status=401
                    )
                return redirect(login_url or 'login')

            if not user_has_permission(request.user, permission_codename):
                if json_response:
                    return JsonResponse(
                        {'error': message or 'Permission denied'}, 
                        status=403
                    )
                
                if message:
                    messages.error(request, message)
                return redirect(login_url or reverse_lazy('home'))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_roles(roles, login_url=None, message=None, json_response=False):
    """
    Décorateur pour vérifier si un utilisateur a un des rôles spécifiés.
    """
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if json_response:
                    return JsonResponse(
                        {'error': 'Authentication required'}, 
                        status=401
                    )
                return redirect(login_url or 'login')

            from .models import user_has_role
            
            has_role = any(user_has_role(request.user, role) for role in roles)
            
            if not has_role and not request.user.is_superuser:
                if json_response:
                    return JsonResponse(
                        {'error': message or 'Accès non autorisé'}, 
                        status=403
                    )
                
                if message:
                    messages.error(request, message)
                return redirect(login_url or reverse_lazy('home'))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_ajax(view_func):
    """
    Décorateur pour s'assurer que la requête est une requête AJAX.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponseForbidden('Accès non autorisé')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
