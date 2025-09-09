from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'
    verbose_name = "Gestion des Rôles et Permissions"
    
    def ready(self):
        # Importer les signaux ici pour éviter les imports circulaires
        from . import signals  # noqa
