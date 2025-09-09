from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.liste_taches, name='liste'),
    path('creer/', views.creer_tache, name='creer'),
    path('<int:tache_id>/', views.detail_tache, name='detail'),
    path('<int:tache_id>/modifier/', views.modifier_tache, name='modifier'),
    path('<int:tache_id>/supprimer/', views.supprimer_tache, name='supprimer'),
    path('<int:tache_id>/changer-statut/<str:nouveau_statut>/', views.changer_statut_tache, name='changer_statut'),
    path('<int:tache_id>/marquer-terminee/', views.marquer_terminee, name='marquer_terminee'),
]
