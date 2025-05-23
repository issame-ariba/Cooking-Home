from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe, Category, Rating, Comment
from django.core.files.uploadedfile import SimpleUploadedFile

class RecipeTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Créer une catégorie de test
        self.category = Category.objects.create(
            name='Desserts',
            description='Recettes de desserts'
        )
        
        # Créer une recette de test
        self.recipe = Recipe.objects.create(
            title='Gâteau au chocolat',
            author=self.user,
            category=self.category,
            description='Un délicieux gâteau au chocolat',
            ingredients='200g chocolat\n200g beurre\n200g sucre\n4 oeufs',
            instructions='1. Faire fondre le chocolat\n2. Mélanger les ingrédients\n3. Cuire',
            preparation_time=20,
            cooking_time=30,
            servings=8,
            difficulty='medium'
        )
        
        # Créer un client de test
        self.client = Client()

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, 'Gâteau au chocolat')
        self.assertEqual(self.recipe.author, self.user)
        self.assertEqual(self.recipe.category, self.category)

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertContains(response, 'Gâteau au chocolat')

    def test_recipe_detail_view(self):
        response = self.client.get(
            reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, self.recipe.title)

    def test_recipe_create_view(self):
        # Se connecter
        self.client.login(username='testuser', password='testpass123')
        # Données de la nouvelle recette
        data = {
            'title': 'Tarte aux pommes',
            'category': self.category.id,
            'description': 'Une délicieuse tarte aux pommes',
            'ingredients': '6 pommes\n1 pâte brisée\n100g sucre',
            'instructions': '1. Éplucher les pommes\n2. Préparer la pâte\n3. Cuire',
            'preparation_time': 30,
            'cooking_time': 45,
            'servings': 6,
            'difficulty': 'easy',
            'tags': ''
        }
        response = self.client.post(reverse('recipes:recipe_create'), data, follow=True)
        self.assertEqual(response.status_code, 200)  # 200 car on suit la redirection
        self.assertTrue(Recipe.objects.filter(title='Tarte aux pommes').exists())

    def test_recipe_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Gâteau au chocolat modifié',
            'category': self.category.id,
            'description': self.recipe.description,
            'ingredients': self.recipe.ingredients,
            'instructions': self.recipe.instructions,
            'preparation_time': self.recipe.preparation_time,
            'cooking_time': self.recipe.cooking_time,
            'servings': self.recipe.servings,
            'difficulty': self.recipe.difficulty,
            'tags': ''
        }
        response = self.client.post(
            reverse('recipes:recipe_edit', kwargs={'pk': self.recipe.pk}),
            data,
            follow=True
        )
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Gâteau au chocolat modifié')

    def test_recipe_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('recipes:recipe_delete', kwargs={'pk': self.recipe.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_recipe_search(self):
        # Recherche qui doit trouver la recette
        response = self.client.get(reverse('recipes:search'), {'query': 'chocolat'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gâteau au chocolat')
        # Recherche qui ne doit pas trouver la recette
        response = self.client.get(reverse('recipes:search'), {'query': 'introuvable'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Gâteau au chocolat')

class RatingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            author=self.user,
            description='Test Description',
            ingredients='Test Ingredients',
            instructions='Test Instructions',
            preparation_time=30,
            cooking_time=30,
            servings=4,
            difficulty='easy'
        )
        self.client = Client()

    def test_rating_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('recipes:rate_recipe', kwargs={'pk': self.recipe.pk}),
            {'value': 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().value, 5)

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            author=self.user,
            description='Test Description',
            ingredients='Test Ingredients',
            instructions='Test Instructions',
            preparation_time=30,
            cooking_time=30,
            servings=4,
            difficulty='easy'
        )
        self.client = Client()

    def test_comment_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('recipes:add_comment', kwargs={'pk': self.recipe.pk}),
            {'content': 'Test Comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'Test Comment')
