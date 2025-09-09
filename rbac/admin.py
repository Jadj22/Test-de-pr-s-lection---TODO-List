from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Role, UserRole

User = get_user_model()


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'user' in self.fields:
            self.fields['user'].queryset = User.objects.all()
        if 'created_by' in self.fields:
            self.fields['created_by'].queryset = User.objects.all()


class UserRoleInline(admin.TabularInline):
    model = UserRole
    form = UserRoleForm
    extra = 1
    verbose_name = _("Rôle utilisateur")
    verbose_name_plural = _("Rôles utilisateur")
    fk_name = 'user'


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_permissions_count')
    search_fields = ('name', 'description')
    filter_horizontal = ('permissions',)
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = _("Nombre de permissions")


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'role', 'created_at', 'created_by')
    list_filter = ('role', 'created_at')
    search_fields = ('user__email', 'role__name')
    readonly_fields = ('created_at',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email Utilisateur'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# Enregistrer les modèles RBAC
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)

# Vérifier si le modèle User est déjà enregistré avant de le personnaliser
if admin.site.is_registered(User):
    admin.site.unregister(User)

# Personnaliser l'interface d'administration de l'utilisateur
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (UserRoleInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'get_roles')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_roles(self, obj):
        return ", ".join([ur.role.name for ur in obj.user_roles.all()])
    get_roles.short_description = _("Rôles")

# Enregistrer le modèle User avec la personnalisation
admin.site.register(User, CustomUserAdmin)

# Personnaliser le modèle Group
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_role')
    filter_horizontal = ('permissions',)
    
    def get_role(self, obj):
        try:
            return obj.role
        except:
            return None
    get_role.short_description = _("Rôle associé")

# Vérifier si le modèle Group est déjà enregistré avant de le personnaliser
if admin.site.is_registered(Group):
    admin.site.unregister(Group)

# Enregistrer le modèle Group avec la personnalisation
admin.site.register(Group, GroupAdmin)
