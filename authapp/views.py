from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import User

def inscription(request):
    """Vue pour l'inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        
        # Validation des données
        if password != confirmation:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'authapp/inscription.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cette adresse email est déjà utilisée.')
            return render(request, 'authapp/inscription.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
            return render(request, 'authapp/inscription.html')
        
        # Création de l'utilisateur
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=prenom,
                last_name=nom,
                password=password
            )
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('connexion')
        except Exception as e:
            messages.error(request, f'Une erreur est survenue lors de l\'inscription : {str(e)}')
    
    return render(request, 'authapp/inscription.html')

def connexion_view(request):
    """Vue pour la connexion d'un utilisateur"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('tableau_de_bord')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    
    return render(request, 'authapp/connexion.html')

@login_required
def deconnexion_view(request):
    """Vue pour la déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('authapp:connexion')

@login_required
def profil_view(request):
    """Vue pour afficher et modifier le profil utilisateur"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('prenom', user.first_name)
        user.last_name = request.POST.get('nom', user.last_name)
        
        # Vérification si l'email est déjà utilisé
        new_email = request.POST.get('email')
        if new_email != user.email and User.objects.filter(email=new_email).exists():
            messages.error(request, 'Cette adresse email est déjà utilisée.')
        else:
            user.email = new_email
            
            # Mise à jour du mot de passe si fourni
            nouveau_mot_de_passe = request.POST.get('nouveau_mot_de_passe')
            if nouveau_mot_de_passe:
                user.set_password(nouveau_mot_de_passe)
            
            user.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            
            # Si le mot de passe a été changé, il faut reconnecter l'utilisateur
            if nouveau_mot_de_passe:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
    
    return render(request, 'authapp/profil.html')
