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

## Captures des interfaces

![Capture](/static_src/capture.png)

## 🚀 Tester avec Postman

### Configuration initiale

1. **Importer la collection**
   - Téléchargez la collection Postman depuis le dossier `postman/`
   - Importez-la dans Postman

2. **Configurer l'environnement**
   - Créez un nouvel environnement "TodoList Local"
   - Ajoutez ces variables :
     - `base_url`: `http://localhost:8000`
     - `token`: (laissez vide)

### Authentification

#### 1. Inscription d'un nouvel utilisateur

```http
POST {{base_url}}/api/inscription/
Content-Type: application/json

{
    "email": "utilisateur@example.com",
    "password": "motdepasse123",
    "password2": "motdepasse123",
    "first_name": "Prénom",
    "last_name": "Nom"
}
```

**Réponse attendue :**
```json
{
    "email": "utilisateur@example.com",
    "first_name": "Prénom",
    "last_name": "Nom"
}
```

#### 2. Connexion (Obtenir un token JWT)

```http
POST {{base_url}}/api/token/
Content-Type: application/json

{
    "email": "utilisateur@example.com",
    "password": "votre_mot_de_passe"
}
```

**Tests (à ajouter dans l'onglet Tests) :**
```javascript
if (pm.response.code === 200) {
    const jsonData = pm.response.json();
    pm.environment.set('token', jsonData.access);
    pm.test("Token reçu", function() {
        pm.expect(jsonData.access).to.not.be.undefined;
    });
}
```

### Endpoints Tâches

#### 1. Lister les tâches
```http
GET {{base_url}}/api/taches/
Authorization: Bearer {{token}}
```

#### 2. Créer une tâche
```http
POST {{base_url}}/api/taches/
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "titre": "Ma nouvelle tâche",
    "description": "Description de la tâche",
    "date_echeance": "2025-12-31",
    "priorite": "moyenne"
}
```

#### 3. Mettre à jour une tâche
```http
PUT {{base_url}}/api/taches/1/
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "titre": "Tâche mise à jour",
    "description": "Nouvelle description",
    "termine": true
}
```

#### 4. Basculer l'état d'une tâche
```http
POST {{base_url}}/api/taches/1/toggle_complete/
Authorization: Bearer {{token}}
```

#### 5. Supprimer une tâche
```http
DELETE {{base_url}}/api/taches/1/
Authorization: Bearer {{token}}
```

### Endpoints Projets

#### 1. Lister les projets
```http
GET {{base_url}}/api/projets/
Authorization: Bearer {{token}}
```

#### 2. Créer un projet
```http
POST {{base_url}}/api/projets/
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "titre": "Nouveau projet",
    "description": "Description du projet"
}
```

### Exécution des tests

1. **Ordre recommandé** :
   1. Authentification (pour obtenir le token)
   2. Créer un projet
   3. Créer une tâche
   4. Lister les tâches
   5. Mettre à jour une tâche
   6. Basculer l'état d'une tâche
   7. Supprimer une tâche

2. **Variables d'environnement** :
   - Le token JWT est automatiquement enregistré après l'authentification
   - Utilisez `{{base_url}}` pour l'URL de base
   - Utilisez `{{token}}` pour le jeton d'authentification