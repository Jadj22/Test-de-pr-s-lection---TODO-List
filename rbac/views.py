from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, View
)

from .models import Role, UserRole
from .decorators import require_permission


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est un membre du personnel."""
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect(reverse_lazy('admin:login') + f'?next={self.request.path}')


class RoleListView(StaffRequiredMixin, ListView):
    """Vue pour lister tous les rôles."""
    model = Role
    template_name = 'rbac/role_list.html'
    context_object_name = 'roles'
    paginate_by = 20


class RoleCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """Vue pour créer un nouveau rôle."""
    model = Role
    fields = ['name', 'description', 'permissions']
    template_name = 'rbac/role_form.html'
    success_url = reverse_lazy('rbac:role_list')
    success_message = _("Le rôle a été créé avec succès.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Grouper les permissions par application
        form.fields['permissions'].queryset = form.fields['permissions'].queryset.order_by('content_type__app_label', 'name')
        return form


class RoleUpdateView(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    """Vue pour modifier un rôle existant."""
    model = Role
    fields = ['name', 'description', 'permissions']
    template_name = 'rbac/role_form.html'
    success_url = reverse_lazy('rbac:role_list')
    success_message = _("Le rôle a été mis à jour avec succès.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Grouper les permissions par application
        form.fields['permissions'].queryset = form.fields['permissions'].queryset.order_by('content_type__app_label', 'name')
        return form


class RoleDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    """Vue pour supprimer un rôle."""
    model = Role
    template_name = 'rbac/role_confirm_delete.html'
    success_url = reverse_lazy('rbac:role_list')
    success_message = _("Le rôle a été supprimé avec succès.")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class RoleDetailView(StaffRequiredMixin, DetailView):
    """Vue pour afficher les détails d'un rôle."""
    model = Role
    template_name = 'rbac/role_detail.html'
    context_object_name = 'role'


class UserRoleListView(StaffRequiredMixin, ListView):
    """Vue pour lister les rôles d'un utilisateur."""
    model = UserRole
    template_name = 'rbac/user_role_list.html'
    context_object_name = 'user_roles'
    paginate_by = 20

    def get_queryset(self):
        self.user = get_object_or_404(get_user_model(), pk=self.kwargs['user_id'])
        return UserRole.objects.filter(user=self.user).select_related('role', 'created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_obj'] = self.user
        return context


class UserRoleCreateView(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """Vue pour attribuer un rôle à un utilisateur."""
    model = UserRole
    fields = ['role']
    template_name = 'rbac/user_role_form.html'
    success_message = _("Le rôle a été attribué à l'utilisateur avec succès.")

    def get_success_url(self):
        return reverse_lazy('rbac:user_role_list', kwargs={'user_id': self.kwargs['user_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(get_user_model(), pk=self.kwargs['user_id'])
        # Exclure les rôles déjà attribués à l'utilisateur
        context['form'].fields['role'].queryset = Role.objects.exclude(
            user_roles__user_id=self.kwargs['user_id']
        )
        return context

    def form_valid(self, form):
        form.instance.user_id = self.kwargs['user_id']
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UserRoleDeleteView(StaffRequiredMixin, SuccessMessageMixin, DeleteView):
    """Vue pour supprimer un rôle d'un utilisateur."""
    model = UserRole
    template_name = 'rbac/user_role_confirm_delete.html'
    success_message = _("Le rôle a été retiré de l'utilisateur avec succès.")

    def get_success_url(self):
        return reverse_lazy('rbac:user_role_list', kwargs={'user_id': self.object.user_id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# Vues API pour AJAX
class RoleListAPIView(StaffRequiredMixin, View):
    """API pour lister les rôles (AJAX)."""
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search', '')
        roles = Role.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        ).values('id', 'name', 'description')
        return JsonResponse(list(roles), safe=False)


class RolePermissionsAPIView(StaffRequiredMixin, View):
    """API pour lister les permissions d'un rôle (AJAX)."""
    def get(self, request, *args, **kwargs):
        role = get_object_or_404(Role, pk=kwargs['pk'])
        permissions = role.permissions.values('id', 'name', 'codename')
        return JsonResponse(list(permissions), safe=False)


# Vues utilitaires
@require_permission('rbac.view_role')
def role_autocomplete(request):
    """Vue pour l'autocomplétion des rôles."""
    search = request.GET.get('q', '')
    roles = Role.objects.filter(
        Q(name__icontains=search) | Q(description__icontains=search)
    ).values('id', 'name')
    return JsonResponse(list(roles), safe=False)
