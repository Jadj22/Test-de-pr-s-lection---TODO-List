
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView as BaseTemplateView
from django.utils import timezone
from django.db.models import Count, Q
from projects.models import Projet
from tasks.models import Tache
from . import views

class DashboardView(LoginRequiredMixin, BaseTemplateView):
    template_name = 'tableau_de_bord.html'
    
    def get_context_data(self, **kwargs):
        # Vérifier si l'utilisateur est authentifié
        print("=== DÉBUT DEBUG TABLEAU DE BORD ===")
        print(f"Utilisateur authentifié: {self.request.user.is_authenticated}")
        print(f"Utilisateur: {self.request.user}")
        
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Vérifier si l'utilisateur est anonyme
        if user.is_anonymous:
            print("ATTENTION: L'utilisateur n'est pas authentifié")
            return context
        
        # Statistiques des projets
        projets_actifs = Projet.objects.filter(
            proprietaire=user,
            statut='en_cours'
        )
        
        # Statistiques des tâches
        taches_utilisateur = Tache.objects.filter(
            Q(projet__proprietaire=user) | 
            Q(cree_par=user)
        )
        
        taches_terminees = taches_utilisateur.filter(statut='terminee').count()
        taches_en_attente = taches_utilisateur.filter(
            ~Q(statut='terminee') & 
            Q(date_echeance__lt=timezone.now())
        ).count()
        
        # Projets récents (limités à 3)
        projets_recents = Projet.objects.filter(
            proprietaire=user
        ).order_by('-date_creation')[:3]
        
        # Tâches récentes (limitées à 5)
        taches_recentes = Tache.objects.filter(
            Q(projet__proprietaire=user) | 
            Q(cree_par=user)
        ).order_by('-date_creation')[:5]
        
        # Debug information
        print("=== DONNÉES RÉCUPÉRÉES ===")
        print(f"Projets actifs: {projets_actifs.count()}")
        print(f"Tâches utilisateur: {taches_utilisateur.count()}")
        print(f"Tâches terminées: {taches_terminees}")
        print(f"Tâches en attente: {taches_en_attente}")
        print(f"Projets récents: {projets_recents.count()}")
        print(f"Tâches récentes: {taches_recentes.count()}")
        print("=== FIN DONNÉES RÉCUPÉRÉES ===")
        
        context.update({
            'user': user,
            'projets_actifs_count': projets_actifs.count(),
            'taches_terminees_count': taches_terminees,
            'taches_en_attente_count': taches_en_attente,
            'projets_recents': projets_recents,
            'taches_recentes': taches_recentes,
        })
        
        return context

urlpatterns = [
    # URLs d'administration
    path('admin/', admin.site.urls),
    
    # URL de la page d'accueil
    path('', views.accueil, name='accueil'),
    
    # Tableau de bord (protégé par authentification)
    path('dashboard/', DashboardView.as_view(), name='tableau_de_bord'),
    
    # URLs d'authentification
    path('auth/', include('authapp.urls')),
    
    # URLs des projets
    path('projets/', include('projects.urls')),
    
    # URLs des tâches
    path('taches/', include('tasks.urls')),
    
    # Outils de développement
    path("__reload__/", include("django_browser_reload.urls")),
]
