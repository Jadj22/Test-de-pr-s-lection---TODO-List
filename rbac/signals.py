from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

@receiver(post_migrate)
def create_initial_roles_and_permissions(sender, **kwargs):
    """
    Crée les rôles et permissions de base lors de la migration initiale.
    """
    from .models import Role
    
    # Créer les rôles de base s'ils n'existent pas
    roles_permissions = {
        'admin': {
            'description': 'Administrateur avec accès complet au système',
            'permissions': [
                'add_user', 'change_user', 'delete_user', 'view_user',
                'add_group', 'change_group', 'delete_group', 'view_group',
                'add_permission', 'change_permission', 'view_permission',
                'add_role', 'change_role', 'delete_role', 'view_role',
                'add_userrole', 'change_userrole', 'delete_userrole', 'view_userrole',
                # Permissions pour les projets
                'add_project', 'change_project', 'delete_project', 'view_project',
                # Permissions pour les tâches
                'add_task', 'change_task', 'delete_task', 'view_task',
                # Autres permissions spécifiques à votre application
            ]
        },
        'gestionnaire': {
            'description': 'Peut gérer les projets et les tâches',
            'permissions': [
                'add_project', 'change_project', 'view_project',
                'add_task', 'change_task', 'delete_task', 'view_task',
                'view_user',
            ]
        },
        'membre': {
            'description': 'Peut voir et modifier les tâches qui lui sont assignées',
            'permissions': [
                'view_project',
                'view_task', 'change_task',
            ]
        },
        'invite': {
            'description': 'Accès en lecture seule',
            'permissions': [
                'view_project',
                'view_task',
            ]
        },
    }
    
    # Créer les rôles et leurs permissions
    for role_name, role_data in roles_permissions.items():
        role, created = Role.objects.get_or_create(
            name=role_name,
            defaults={'description': role_data['description']}
        )
        
        if created or role.permissions.count() == 0:
            # Ajouter les permissions au rôle
            permissions = []
            for perm_codename in role_data['permissions']:
                try:
                    app_label, codename = perm_codename.split('.')
                    content_type = ContentType.objects.get(app_label=app_label)
                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )
                    permissions.append(perm)
                except (ValueError, Permission.DoesNotExist, ContentType.DoesNotExist):
                    continue
            
            role.permissions.set(permissions)
    
    # Créer le groupe Administrateurs s'il n'existe pas
    admin_group, created = Group.objects.get_or_create(name='Administrateurs')
    if created:
        # Donner toutes les permissions au groupe Administrateurs
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)
        
        # Ajouter le rôle admin au groupe Administrateurs
        try:
            admin_role = Role.objects.get(name='admin')
            admin_group.role = admin_role
            admin_group.save()
        except Role.DoesNotExist:
            pass
