from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Pages principales
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    
    # Gestion des utilisateurs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('favorites/', views.favorites, name='favorites'),
    
    # Interactions avec les recettes
    path('recipe/<int:pk>/rate/', views.recipe_rate, name='recipe_rate'),
    path('recipe/<int:pk>/comment/', views.recipe_comment, name='recipe_comment'),
    path('recipe/<int:pk>/favorite/', views.recipe_favorite, name='toggle_favorite'),
    path('recipe/image/<int:image_id>/delete/', views.delete_recipe_image, name='delete_recipe_image'),
    
    # Catégories
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    
    # Recherche et filtres
    path('search/', views.recipe_search, name='search'),
    path('tag/<slug:tag_slug>/', views.recipe_by_tag, name='recipe_by_tag'),
    
    # API pour le calcul des portions
    path('api/recipe/<int:pk>/adjust-servings/', views.adjust_servings, name='adjust_servings'),
] 