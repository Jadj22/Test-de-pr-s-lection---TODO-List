
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # URLs d'administration
    path('admin/', admin.site.urls),
    
    # URL de la page d'accueil
    path('', views.accueil, name='accueil'),
    
    # Tableau de bord (protégé par authentification)
    path('dashboard/', login_required(TemplateView.as_view(template_name='tableau_de_bord.html')), name='tableau_de_bord'),
    
    # URLs d'authentification
    path('auth/', include('authapp.urls')),
    
    # URLs des projets
    path('projets/', include('projects.urls')),
    
    # URLs des tâches
    path('taches/', include('tasks.urls')),
    
    # Outils de développement
    path("__reload__/", include("django_browser_reload.urls")),
]
