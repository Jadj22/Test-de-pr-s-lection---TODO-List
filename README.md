# 📋 Application de Gestion des Tâches (TODO List)

Une application web complète de gestion des tâches et projets, développée avec Django et Tailwind CSS. Cette application permet aux utilisateurs de créer, gérer et suivre leurs tâches et projets en toute simplicité.

## ✨ Fonctionnalités Principales

### 📂 Gestion des Projets
- Création, édition et suppression de projets
- Suivi de l'état des projets (À faire, En cours, Terminé)
- Vue détaillée de chaque projet avec les tâches associées
- Tableau de bord avec statistiques

### ✅ Gestion des Tâches
- Création, édition et suppression de tâches
- Attribution de priorités et d'échéances
- Filtrage et tri des tâches
- Suivi de l'état d'avancement

### 👤 Gestion des Utilisateurs
- Inscription et authentification
- Profil utilisateur personnalisable
- Tableau de bord personnalisé

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.8 ou supérieur (téléchargeable sur [python.org](https://www.python.org/downloads/))
- pip (inclus avec Python)
- Git ([télécharger Git](https://git-scm.com/downloads))
- Node.js et npm ([télécharger Node.js](https://nodejs.org/))

### Installation pas à pas

1. **Cloner le dépôt**
   ```bash
   # Cloner le dépôt
   git clone https://github.com/Jadj22/Test-de-pr-s-lection---TODO-List.git
   
   # Se déplacer dans le dossier du projet
   cd Test-de-pr-s-lection---TODO-List
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   # Créer un environnement virtuel
   python -m venv venv
   
   # Activer l'environnement virtuel
   # Sur Windows :
   .\venv\Scripts\activate
   # Sur macOS/Linux :
   # source venv/bin/activate
   ```

3. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   # Appliquer les migrations
   python manage.py migrate
   ```

5. **Créer un compte administrateur**
   ```bash
   python manage.py createsuperuser
   # Suivez les invites pour créer un compte administrateur
   ```

6. **Installer les dépendances frontend**
   ```bash
   npm install
   ```

7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

8. **Accéder à l'application**
   - Application : http://127.0.0.1:8000/
   - Interface d'administration : http://127.0.0.1:8000/admin/

### Premier pas
1. Créez un compte via l'interface d'inscription
2. Connectez-vous avec vos identifiants
3. Commencez par créer votre premier projet
4. Ajoutez des tâches à votre projet

## 📊 Structure du Projet

```text
TodoListTest/
├── authapp/              # Application d'authentification
├── projects/             # Gestion des projets
├── tasks/                # Gestion des tâches
├── rbac/                 # Gestion des rôles et permissions
├── theme/                # Thème et assets frontend
├── templates/            # Templates HTML de base
└── todolist/             # Configuration du projet
```

## 👥 Auteurs

- [Jadj22] - Développeur Principal

## Captures des interfaces

![Capture](/static_src/image1.png)
![Capture](/static_src/image2.png)


