# Application de Gestion des Tâches (TODO List)

## 📋 Description

Une application web complète de gestion des tâches et projets, développée avec Django et Tailwind CSS. Cette application permet aux utilisateurs de créer, gérer et suivre leurs tâches et projets en toute simplicité.

## 🚀 Fonctionnalités

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

- Inscription et authentification des utilisateurs
- Profil utilisateur personnalisable
- Tableau de bord personnalisé

### 🎨 Interface Utilisateur Moderne

- Design responsive avec Tailwind CSS
- Interface intuitive et conviviale
- Thème clair/sombre (selon les préférences système)

## 🛠️ Technologies Utilisées

### Backend

- Python 3.x
- Django 4.2
- SQLite (développement) / PostgreSQL (production)

### Frontend

- HTML5, CSS3, JavaScript
- Tailwind CSS 3.x
- Font Awesome pour les icônes

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Node.js et npm (pour les assets frontend)

### Configuration

1. **Cloner le dépôt**

   ```bash
   git clone [URL_DU_DEPOT]
   cd TodoListTest
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**

   Créer un fichier `.env` à la racine du projet avec les variables nécessaires.

5. **Appliquer les migrations**

   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur**

   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**

   ```bash
   python manage.py runserver
   ```

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
