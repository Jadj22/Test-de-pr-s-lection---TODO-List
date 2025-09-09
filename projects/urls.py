from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.liste_projets, name='liste'),
    path('creer/', views.creer_projet, name='creer'),
    path('<int:projet_id>/', views.detail_projet, name='detail'),
    path('<int:projet_id>/modifier/', views.modifier_projet, name='modifier'),
    path('<int:projet_id>/supprimer/', views.supprimer_projet, name='supprimer'),
]
