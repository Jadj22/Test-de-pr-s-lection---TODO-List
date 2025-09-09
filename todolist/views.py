from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def accueil(request):
    """Vue pour la page d'accueil"""
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')
    return render(request, 'accueil.html')

def test_tailwind(request):
    """Vue de test pour Tailwind CSS"""
    return render(request, 'test.html')
