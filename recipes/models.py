from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile')
    ]
    
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    preparation_time = models.PositiveIntegerField(help_text="Temps de préparation en minutes")
    cooking_time = models.PositiveIntegerField(help_text="Temps de cuisson en minutes")
    servings = models.PositiveIntegerField(help_text="Nombre de portions")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cover_image = models.ImageField(upload_to='recipe_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    favorites = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_instructions_list(self):
        """Retourne la liste des instructions, chaque ligne étant une étape."""
        return [line.strip() for line in self.instructions.split('\n') if line.strip()]
    
    class Meta:
        ordering = ['-created_at']

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipes/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image pour {self.recipe.title}"

class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('recipe', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} - {self.value} étoiles"

class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.recipe.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True, help_text="Nom d'affichage public")
    bio = models.TextField(blank=True, help_text="Une brève description de vous")
    specialties = models.TextField(blank=True, help_text="Vos spécialités culinaires")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, help_text="Votre localisation")
    website = models.URLField(blank=True, help_text="Votre site web personnel")
    social_media = models.CharField(max_length=200, blank=True, help_text="Liens vers vos réseaux sociaux")
    
    def __str__(self):
        return self.display_name or self.user.username
    
    def get_full_name(self):
        return self.display_name or f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def get_email(self):
        return self.user.email
