from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

class Role(models.Model):
    """
    Modèle représentant un rôle dans le système RBAC.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du rôle")
    description = models.TextField(blank=True, verbose_name="Description")
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name="permissions",
        related_name="roles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ['name']

    def __str__(self):
        return self.name

    def has_permission(self, perm):
        """Vérifie si le rôle a une permission spécifique."""
        return self.permissions.filter(codename=perm).exists()


class UserRole(models.Model):
    """
    Modèle de liaison entre User et Role avec des métadonnées supplémentaires.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name="Utilisateur"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name="Rôle"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_roles',
        verbose_name="Attribué par"
    )

    class Meta:
        verbose_name = "Rôle utilisateur"
        verbose_name_plural = "Rôles utilisateurs"
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


# Méthodes utilitaires pour gérer les rôles
def assign_role_to_user(user, role_name, created_by=None):
    """
    Attribue un rôle à un utilisateur.
    """
    try:
        role = Role.objects.get(name=role_name)
        user_role, created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            defaults={'created_by': created_by or user}
        )
        return user_role, created
    except Role.DoesNotExist:
        return None, False


def remove_role_from_user(user, role_name):
    """
    Supprime un rôle d'un utilisateur.
    """
    try:
        role = Role.objects.get(name=role_name)
        return UserRole.objects.filter(user=user, role=role).delete()
    except Role.DoesNotExist:
        return False


def user_has_role(user, role_name):
    """
    Vérifie si un utilisateur a un rôle spécifique.
    """
    if not user.is_authenticated:
        return False
    return UserRole.objects.filter(user=user, role__name=role_name).exists()


def user_has_permission(user, permission_codename):
    """
    Vérifie si un utilisateur a une permission spécifique via ses rôles.
    """
    if not user.is_authenticated:
        return False
        
    # Si l'utilisateur est superutilisateur, il a toutes les permissions
    if user.is_superuser:
        return True
        
    # Vérifier les permissions via les rôles
    return Permission.objects.filter(
        Q(roles__user_roles__user=user) & 
        Q(codename=permission_codename)
    ).exists()
