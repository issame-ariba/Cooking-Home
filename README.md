# Plateforme de Partage de Recettes

Une application web Django permettant aux utilisateurs de partager, découvrir et commenter des recettes de cuisine.

## Fonctionnalités

- Gestion des utilisateurs (inscription, connexion, profils)
- Gestion des recettes (création, modification, suppression)
- Système de catégories et tags
- Recherche avancée avec filtres multiples
- Évaluation et commentaires
- Gestion des favoris
- Calcul dynamique des portions
- Interface d'administration
- Interface responsive et moderne
- Tests unitaires complets

## Prérequis

- Python 3.8 ou supérieur
- Django 5.0
- MySQL 8.0 ou supérieur

## Installation

1. Cloner le dépôt :
```bash
git clone <url_du_depot>
cd recipes
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer la base de données MySQL :
- Créer une base de données MySQL
- Copier `.env.example` vers `.env` et configurer les variables d'environnement :
```
DEBUG=True
SECRET_KEY=votre_cle_secrete
DB_NAME=nom_de_la_base
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

5. Appliquer les migrations :
```bash
python manage.py migrate
```

6. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

7. Lancer le serveur de développement :
```bash
python manage.py runserver
```

8. Exécuter les tests :
```bash
python manage.py test
```

## Structure du Projet

```
recipes/
├── cooking_recipes/     # Configuration du projet
├── recipes/            # Application principale
│   ├── migrations/     # Migrations de la base de données
│   ├── static/        # Fichiers statiques (CSS, JS)
│   ├── templates/     # Templates HTML
│   ├── admin.py       # Configuration de l'admin
│   ├── forms.py       # Formulaires
│   ├── models.py      # Modèles de données
│   ├── tests.py       # Tests unitaires
│   ├── urls.py        # Configuration des URLs
│   └── views.py       # Vues et logique métier
├── static/            # Fichiers statiques globaux
├── templates/         # Templates globaux
├── media/            # Fichiers uploadés
├── manage.py         # Script de gestion Django
└── requirements.txt  # Dépendances Python
```

## Fonctionnalités Détaillées

### Gestion des Recettes
- Création de recettes avec titre, description, ingrédients, instructions
- Upload d'images
- Catégorisation et tags
- Temps de préparation et de cuisson
- Niveau de difficulté
- Nombre de portions

### Recherche Avancée
- Recherche par mot-clé
- Filtres par catégorie
- Filtres par temps de préparation
- Filtres par niveau de difficulté
- Filtres par tags

### Interactions Utilisateurs
- Système de notation (1-5 étoiles)
- Commentaires
- Ajout aux favoris
- Calcul dynamique des portions

### Interface Utilisateur
- Design responsive avec Bootstrap 5
- Thème moderne et épuré
- Animations et transitions fluides
- Prévisualisation des images
- Validation des formulaires côté client

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub. 