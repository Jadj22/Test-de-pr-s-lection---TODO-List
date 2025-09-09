from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Projet

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'proprietaire_email', 'statut', 'date_creation', 'date_mise_a_jour')
    list_filter = ('statut', 'date_creation')
    search_fields = ('titre', 'description', 'proprietaire__email')
    list_select_related = ('proprietaire',)
    date_hierarchy = 'date_creation'
    
    def proprietaire_email(self, obj):
        return obj.proprietaire.email
    proprietaire_email.short_description = 'Propriétaire'
    
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'proprietaire')
        }),
        (_('Statut'), {
            'fields': ('statut',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Permet de rendre le propriétaire en lecture seule lors de l'édition
        if obj:
            return self.readonly_fields + ('proprietaire', 'date_creation', 'date_mise_a_jour')
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        # Définit automatiquement le propriétaire du projet lors de la création
        if not obj.pk:
            obj.proprietaire = request.user
        super().save_model(request, obj, form, change)
