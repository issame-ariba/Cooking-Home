from django.core.management.base import BaseCommand
from recipes.models import Category

class Command(BaseCommand):
    help = 'Crée les catégories par défaut pour les recettes'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Entrées',
                'description': 'Recettes pour commencer le repas'
            },
            {
                'name': 'Plats principaux',
                'description': 'Plats principaux et accompagnements'
            },
            {
                'name': 'Desserts',
                'description': 'Desserts et pâtisseries'
            },
            {
                'name': 'Apéritifs',
                'description': 'Recettes pour l\'apéritif'
            },
            {
                'name': 'Soupes',
                'description': 'Soupes et potages'
            },
            {
                'name': 'Salades',
                'description': 'Salades et entrées froides'
            },
            {
                'name': 'Petit-déjeuner',
                'description': 'Recettes pour le petit-déjeuner'
            },
            {
                'name': 'Végétarien',
                'description': 'Recettes végétariennes'
            },
            {
                'name': 'Végan',
                'description': 'Recettes véganes'
            },
            {
                'name': 'Sans gluten',
                'description': 'Recettes sans gluten'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Catégorie "{category_data["name"]}" créée avec succès')
            ) 