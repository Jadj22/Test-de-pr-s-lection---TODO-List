from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Tache

class TacheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'projet', 'afficher_proprietaire', 'afficher_assigne_a', 'statut', 'date_echeance', 'est_terminee')
    list_filter = ('statut', 'date_echeance', 'projet')
    search_fields = ('titre', 'description', 'projet__titre', 'cree_par__username', 'assigne_a__username')
    list_select_related = ('projet', 'cree_par', 'assigne_a')
    date_hierarchy = 'date_creation'
    list_editable = ('statut',)
    
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'projet')
        }),
        (_('Assignation et statut'), {
            'fields': ('assigne_a', 'statut', 'priorite')
        }),
        (_('Dates'), {
            'fields': ('date_echeance', 'date_accomplissement')
        }),
    )
    
    def afficher_proprietaire(self, obj):
        return obj.projet.proprietaire.get_full_name() or obj.projet.proprietaire.username
    afficher_proprietaire.short_description = _('Propriétaire')
    afficher_proprietaire.admin_order_field = 'projet__proprietaire__username'
    
    def afficher_assigne_a(self, obj):
        if obj.assigne_a:
            return obj.assigne_a.get_full_name() or obj.assigne_a.username
        return _('Non assignée')
    afficher_assigne_a.short_description = _('Assignée à')
    afficher_assigne_a.admin_order_field = 'assigne_a__username'
    
    def est_terminee(self, obj):
        return obj.statut == 'terminee'
    est_terminee.boolean = True
    est_terminee.short_description = _('Terminée')
    
    def get_readonly_fields(self, request, obj=None):
        # Rendre certains champs en lecture seule lors de l'édition
        if obj:
            return self.readonly_fields + ('cree_par', 'date_creation')
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        # Définir automatiquement l'utilisateur qui crée la tâche
        if not obj.pk:
            obj.cree_par = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        # Filtrer les tâches pour ne montrer que celles des projets de l'utilisateur
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(projet__proprietaire=request.user)

admin.site.register(Tache, TacheAdmin)
