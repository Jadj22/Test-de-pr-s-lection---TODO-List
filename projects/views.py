from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projet

@login_required
def liste_projets(request):
    """Affiche la liste des projets de l'utilisateur"""
    projets = Projet.objects.filter(proprietaire=request.user).order_by('-date_creation')
    return render(request, 'projects/liste.html', {'projets': projets})

@login_required
def creer_projet(request):
    """Crée un nouveau projet"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        
        if not titre:
            messages.error(request, 'Le titre du projet est requis.')
            return render(request, 'projects/creer.html')
            
        try:
            projet = Projet.objects.create(
                titre=titre,
                description=description,
                proprietaire=request.user
            )
            messages.success(request, 'Le projet a été créé avec succès !')
            return redirect('projects:detail', projet_id=projet.id)
        except Exception as e:
            messages.error(request, f'Une erreur est survenue : {str(e)}')
    
    return render(request, 'projects/creer.html')

@login_required
def detail_projet(request, projet_id):
    """Affiche les détails d'un projet"""
    projet = get_object_or_404(Projet, id=projet_id, proprietaire=request.user)
    return render(request, 'projects/detail.html', {'projet': projet})

@login_required
def modifier_projet(request, projet_id):
    """Modifie un projet existant"""
    projet = get_object_or_404(Projet, id=projet_id, proprietaire=request.user)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        statut = request.POST.get('statut', projet.statut)
        
        if not titre:
            messages.error(request, 'Le titre du projet est requis.')
        else:
            try:
                projet.titre = titre
                projet.description = description
                projet.statut = statut
                projet.save()
                messages.success(request, 'Le projet a été mis à jour avec succès !')
                return redirect('projects:detail', projet_id=projet.id)
            except Exception as e:
                messages.error(request, f'Une erreur est survenue : {str(e)}')
    
    return render(request, 'projects/modifier.html', {'projet': projet})

@login_required
def supprimer_projet(request, projet_id):
    """Supprime un projet"""
    projet = get_object_or_404(Projet, id=projet_id, proprietaire=request.user)
    
    if request.method == 'POST':
        try:
            projet.delete()
            messages.success(request, 'Le projet a été supprimé avec succès.')
            return redirect('projects:liste')
        except Exception as e:
            messages.error(request, f'Une erreur est survenue lors de la suppression : {str(e)}')
    
    return render(request, 'projects/supprimer.html', {'projet': projet})
