from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from .models import Tache
from projects.models import Projet

@login_required
def liste_taches(request):
    """Affiche la liste des tâches de l'utilisateur"""
    taches = Tache.objects.filter(
        projet__proprietaire=request.user
    ).select_related('projet').order_by('-date_creation')
    
    # Filtrage par statut si spécifié
    statut = request.GET.get('statut')
    if statut in dict(Tache.StatutTache.choices):
        taches = taches.filter(statut=statut)
    
    return render(request, 'tasks/liste.html', {
        'taches': taches,
        'statut_filtre': statut
    })

@login_required
def creer_tache(request):
    """Crée une nouvelle tâche"""
    # Récupérer les projets de l'utilisateur pour le formulaire
    projets = Projet.objects.filter(proprietaire=request.user)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        projet_id = request.POST.get('projet')
        date_echeance = request.POST.get('date_echeance')
        
        if not titre or not projet_id:
            messages.error(request, 'Le titre et le projet sont obligatoires.')
        else:
            try:
                projet = Projet.objects.get(id=projet_id, proprietaire=request.user)
                tache = Tache.objects.create(
                    titre=titre,
                    description=description,
                    projet=projet,
                    cree_par=request.user,
                    date_echeance=date_echeance if date_echeance else None
                )
                
                # Gestion de l'assignation si spécifiée
                assigne_a_id = request.POST.get('assigne_a')
                if assigne_a_id:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    try:
                        tache.assigne_a = User.objects.get(id=assigne_a_id)
                        tache.save()
                    except User.DoesNotExist:
                        pass
                
                messages.success(request, 'La tâche a été créée avec succès !')
                return redirect('tasks:detail', tache_id=tache.id)
                
            except Projet.DoesNotExist:
                messages.error(request, 'Projet invalide.')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue : {str(e)}')
    
    return render(request, 'tasks/creer.html', {
        'projets': projets,
        'statuts': Tache.StatutTache.choices
    })

import logging

logger = logging.getLogger(__name__)

@login_required
def detail_tache(request, tache_id):
    """Affiche les détails d'une tâche"""
    tache = get_object_or_404(
        Tache.objects.select_related('projet', 'cree_par', 'assigne_a'),
        id=tache_id,
        projet__proprietaire=request.user
    )
    
    # Log pour le débogage
    logger.debug(f"Tâche chargée - ID: {tache.id}, Créée par: {tache.cree_par}")
    if tache.cree_par:
        logger.debug(f"Détails de l'utilisateur - ID: {tache.cree_par.id}, Username: {tache.cree_par.username}, Full name: {getattr(tache.cree_par, 'get_full_name', lambda: 'N/A')()}")
    
    return render(request, 'tasks/detail.html', {'tache': tache})

@login_required
def modifier_tache(request, tache_id):
    """Modifie une tâche existante"""
    tache = get_object_or_404(
        Tache,
        id=tache_id,
        projet__proprietaire=request.user
    )
    
    projets = Projet.objects.filter(proprietaire=request.user)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        projet_id = request.POST.get('projet')
        statut = request.POST.get('statut', tache.statut)
        date_echeance = request.POST.get('date_echeance')
        assigne_a_id = request.POST.get('assigne_a')
        
        if not titre or not projet_id:
            messages.error(request, 'Le titre et le projet sont obligatoires.')
        else:
            try:
                projet = Projet.objects.get(id=projet_id, proprietaire=request.user)
                
                tache.titre = titre
                tache.description = description
                tache.projet = projet
                tache.statut = statut
                tache.date_echeance = date_echeance if date_echeance else None
                
                # Gestion de l'assignation
                if assigne_a_id:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    try:
                        tache.assigne_a = User.objects.get(id=assigne_a_id)
                    except User.DoesNotExist:
                        tache.assigne_a = None
                else:
                    tache.assigne_a = None
                
                tache.save()
                messages.success(request, 'La tâche a été mise à jour avec succès !')
                return redirect('tasks:detail', tache_id=tache.id)
                
            except Projet.DoesNotExist:
                messages.error(request, 'Projet invalide.')
            except Exception as e:
                messages.error(request, f'Une erreur est survenue : {str(e)}')
    
    return render(request, 'tasks/modifier.html', {
        'tache': tache,
        'projets': projets,
        'statuts': Tache.StatutTache.choices
    })

@login_required
def supprimer_tache(request, tache_id):
    """Supprime une tâche"""
    tache = get_object_or_404(
        Tache,
        id=tache_id,
        projet__proprietaire=request.user
    )
    
    if request.method == 'POST':
        try:
            tache.delete()
            messages.success(request, 'La tâche a été supprimée avec succès.')
            return redirect('tasks:liste')
        except Exception as e:
            messages.error(request, f'Une erreur est survenue : {str(e)}')
    
    return render(request, 'tasks/supprimer.html', {'tache': tache})

@login_required
def changer_statut_tache(request, tache_id, nouveau_statut):
    """
    Change le statut d'une tâche (utilisé pour les actions rapides).
    Si nouveau_statut est 'toggle', bascule entre 'termine' et 'en_cours'.
    """
    if request.method == 'POST' and request.headers.get('HX-Request') == 'true':
        try:
            tache = Tache.objects.get(
                id=tache_id,
                projet__proprietaire=request.user
            )
            
            # Gérer le cas du toggle
            if nouveau_statut == 'toggle':
                tache.termine = not tache.termine
                tache.statut = 'termine' if tache.termine else 'en_cours'
            # Vérifier que le statut est valide
            elif nouveau_statut in dict(Tache.StatutTache.choices):
                tache.statut = nouveau_statut
                tache.termine = (nouveau_statut == 'termine')
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Statut non valide'
                }, status=400)
            
            tache.save()
            
            return JsonResponse({
                'success': True,
                'statut_display': tache.get_statut_display(),
                'termine': tache.termine,
                'statut': tache.statut
            })
            
        except Tache.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Tâche non trouvée ou accès non autorisé'
            }, status=404)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Requête invalide'
    }, status=400)

@login_required
def marquer_terminee(request, tache_id):
    """Marque une tâche comme terminée ou non (utilisé avec HTMX)"""
    if request.method == 'POST':
        tache = get_object_or_404(Tache, id=tache_id, projet__proprietaire=request.user)
        
        # Basculer entre 'terminee' et 'a_faire'
        if tache.statut == Tache.StatutTache.TERMINEE:
            tache.statut = Tache.StatutTache.A_FAIRE
        else:
            tache.statut = Tache.StatutTache.TERMINEE
            from django.utils import timezone
            tache.date_accomplissement = timezone.now()
            
        tache.save()
        
        # Retourner une réponse vide avec un code 200 pour HTMX
        return HttpResponse()
    
    return HttpResponseNotAllowed(['POST'])
