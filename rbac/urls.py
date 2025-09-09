from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import views

app_name = 'rbac'

urlpatterns = [
    # URLs pour la gestion des rôles
    path('roles/', 
         staff_member_required(views.RoleListView.as_view()), 
         name='role_list'),
    path('roles/ajouter/', 
         staff_member_required(views.RoleCreateView.as_view()), 
         name='role_create'),
    path('roles/<int:pk>/', 
         staff_member_required(views.RoleDetailView.as_view()), 
         name='role_detail'),
    path('roles/<int:pk>/modifier/', 
         staff_member_required(views.RoleUpdateView.as_view()), 
         name='role_update'),
    path('roles/<int:pk>/supprimer/', 
         staff_member_required(views.RoleDeleteView.as_view()), 
         name='role_delete'),
    
    # URLs pour la gestion des rôles utilisateur
    path('utilisateurs/<int:user_id>/roles/', 
         staff_member_required(views.UserRoleListView.as_view()), 
         name='user_role_list'),
    path('utilisateurs/<int:user_id>/roles/ajouter/', 
         staff_member_required(views.UserRoleCreateView.as_view()), 
         name='user_role_create'),
    path('utilisateurs/roles/<int:pk>/supprimer/', 
         staff_member_required(views.UserRoleDeleteView.as_view()), 
         name='user_role_delete'),
    
    # API pour la gestion des rôles (AJAX)
    path('api/roles/', 
         staff_member_required(views.RoleListAPIView.as_view()), 
         name='api_role_list'),
    path('api/roles/<int:pk>/permissions/', 
         staff_member_required(views.RolePermissionsAPIView.as_view()), 
         name='api_role_permissions'),
]
