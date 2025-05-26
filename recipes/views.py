from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg
from django.core.paginator import Paginator
from .models import Recipe, Category, UserProfile, RecipeImage, RecipeRating, RecipeComment
from .forms import (RecipeForm, UserRegistrationForm, UserProfileForm, 
                   RecipeSearchForm, RecipeCommentForm)
from django.views.generic import ListView
from django.db.models import Q

def recipe_list(request):
    search_form = RecipeSearchForm()
    recipes = Recipe.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    if request.GET:
        search_form = RecipeSearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            category = search_form.cleaned_data.get('category')
            difficulty = search_form.cleaned_data.get('difficulty')
            preparation_time = search_form.cleaned_data.get('preparation_time')
            
            if query:
                recipes = recipes.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query)
                )
            if category:
                recipes = recipes.filter(category=category)
            if difficulty:
                recipes = recipes.filter(difficulty=difficulty)
            if preparation_time:
                recipes = recipes.filter(preparation_time__lte=preparation_time)
    
    paginator = Paginator(recipes, 12)  # 12 recettes par page
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'search_form': search_form,
        'categories': categories
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Récupérer la note de l'utilisateur connecté s'il est authentifié
    user_rating = None
    if request.user.is_authenticated:
        user_rating = recipe.ratings.filter(user=request.user).first()
    
    # Récupérer tous les commentaires et les notes
    comments = recipe.comments.all().order_by('-created_at')
    ratings = recipe.ratings.all()
    
    # Calculer la moyenne des notes
    avg_rating = recipe.ratings.aggregate(Avg('value'))['value__avg'] or 0
    
    comment_form = RecipeCommentForm()
    
    # Formater les ingrédients et les instructions
    ingredients_list = [line.strip() for line in recipe.ingredients.split('\n') if line.strip()]
    instructions_list = [line.strip() for line in recipe.instructions.split('\n') if line.strip()]
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'user_rating': user_rating,
        'comments': comments,
        'ratings': ratings,
        'avg_rating': round(avg_rating, 1),
        'comment_form': comment_form,
        'ingredients_list': ingredients_list,
        'instructions_list': instructions_list
    })

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Pour sauvegarder les tags

            # Gestion des images
            images = request.FILES.getlist('images')
            if images:
                # La première image sera l'image principale
                for i, image in enumerate(images):
                    RecipeImage.objects.create(
                        recipe=recipe,
                        image=image,
                        is_primary=(i == 0)  # La première image est l'image principale
                    )

            messages.success(request, 'Recette créée avec succès!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette recette.")
        return redirect('recipes:recipe_detail', pk=pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            try:
                recipe = form.save()
                
                # Gestion des images
                images = request.FILES.getlist('images')
                if images:
                    # Supprimer les anciennes images si nécessaire
                    if 'delete_images' in request.POST:
                        recipe.images.all().delete()
                    
                    # Ajouter les nouvelles images
                    for image in images:
                        RecipeImage.objects.create(
                            recipe=recipe,
                            image=image,
                            is_primary=(not recipe.images.exists())  # La première image est l'image principale
                        )
                
                messages.success(request, 'Recette modifiée avec succès!')
                return redirect('recipes:recipe_detail', pk=recipe.pk)
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de la modification de la recette : {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'recipe': recipe
    })

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette recette.")
        return redirect('recipes:recipe_detail', pk=pk)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recette supprimée avec succès!')
        return redirect('recipes:recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Inscription réussie! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'recipes/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    # Récupérer le profil de l'utilisateur
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Récupérer les recettes de l'utilisateur
    recipes = Recipe.objects.filter(author=request.user)
    
    # Récupérer les recettes favorites
    favorites = request.user.favorite_recipes.all()
    
    # Calculer les statistiques
    recipes_count = recipes.count()
    favorites_count = favorites.count()
    comments_count = RecipeComment.objects.filter(user=request.user).count()
    
    # Pagination des favoris
    paginator = Paginator(favorites, 6)  # 6 recettes par page
    page = request.GET.get('page')
    favorites = paginator.get_page(page)
    
    context = {
        'profile': profile,
        'recipes': recipes,
        'favorites': favorites,
        'recipes_count': recipes_count,
        'favorites_count': favorites_count,
        'comments_count': comments_count,
    }
    
    return render(request, 'recipes/profile.html', context)

@login_required
def profile_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('recipes:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'recipes/profile_edit.html', {'form': form})

@login_required
def recipe_rate(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        value = int(request.POST.get('value', 0))
        if 1 <= value <= 5:
            rating, created = RecipeRating.objects.get_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'value': value}
            )
            if not created:
                rating.value = value
                rating.save()
            
            # Calculer la nouvelle moyenne
            avg_rating = recipe.ratings.aggregate(Avg('value'))['value__avg'] or 0
            return JsonResponse({
                'success': True,
                'avg_rating': round(avg_rating, 1)
            })
    return JsonResponse({'success': False})

@login_required
def recipe_comment(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            messages.success(request, 'Votre commentaire a été publié avec succès.')
        else:
            messages.error(request, 'Une erreur est survenue lors de la publication du commentaire.')
    return redirect('recipes:recipe_detail', pk=pk)

@login_required
def recipe_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
        is_favorite = False
    else:
        recipe.favorites.add(request.user)
        is_favorite = True
    return JsonResponse({'success': True, 'is_favorite': is_favorite})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    recipes = Recipe.objects.filter(category=category)
    paginator = Paginator(recipes, 12)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'recipes/category_detail.html', {
        'category': category,
        'recipes': recipes
    })

def recipe_search(request):
    form = RecipeSearchForm(request.GET)
    recipes = Recipe.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        difficulty = form.cleaned_data.get('difficulty')
        preparation_time = form.cleaned_data.get('preparation_time')
        
        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        if category:
            recipes = recipes.filter(category=category)
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        if preparation_time:
            recipes = recipes.filter(preparation_time__lte=preparation_time)
    
    paginator = Paginator(recipes, 12)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    query = request.GET.get('query', '')
    return render(request, 'recipes/recipe_search.html', {
        'form': form,
        'recipes': recipes,
        'query': query
    })

def recipe_by_tag(request, tag_slug):
    recipes = Recipe.objects.filter(tags__slug=tag_slug)
    paginator = Paginator(recipes, 12)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'recipes/recipe_by_tag.html', {
        'tag_slug': tag_slug,
        'recipes': recipes
    })

def adjust_servings(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    try:
        new_servings = int(request.GET.get('servings', recipe.servings))
        ratio = new_servings / recipe.servings
        
        # Cette fonction devrait être implémentée pour ajuster les quantités
        # des ingrédients en fonction du ratio
        adjusted_ingredients = adjust_ingredients(recipe.ingredients, ratio)
        
        return JsonResponse({
            'success': True,
            'adjusted_ingredients': adjusted_ingredients
        })
    except (ValueError, ZeroDivisionError):
        return JsonResponse({'success': False}, status=400)

def adjust_ingredients(ingredients_text, ratio):
    # Cette fonction devrait implémenter la logique d'ajustement des quantités
    # Pour l'instant, nous retournons juste le texte original
    # TODO: Implémenter la logique d'ajustement des quantités
    return ingredients_text

class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'recipes/search.html'
    context_object_name = 'recipes'
    paginate_by = 9
    
    def get_queryset(self):
        form = RecipeSearchForm(self.request.GET)
        queryset = Recipe.objects.all()
        
        if form.is_valid():
            q = form.cleaned_data.get('q')
            category = form.cleaned_data.get('category')
            difficulty = form.cleaned_data.get('difficulty')
            max_preparation_time = form.cleaned_data.get('max_preparation_time')
            tags = form.cleaned_data.get('tags')
            
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q) |
                    Q(ingredients__icontains=q)
                )
            
            if category:
                queryset = queryset.filter(category=category)
            
            if difficulty:
                queryset = queryset.filter(difficulty=difficulty)
            
            if max_preparation_time:
                queryset = queryset.filter(preparation_time__lte=max_preparation_time)
            
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]
                queryset = queryset.filter(tags__name__in=tag_list).distinct()
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RecipeSearchForm(self.request.GET)
        return context

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    paginator = Paginator(recipes, 12)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'recipes/my_recipes.html', {
        'recipes': recipes
    })

@login_required
def favorites(request):
    favorites = Recipe.objects.filter(favorites=request.user).order_by('-created_at')
    paginator = Paginator(favorites, 12)  # 12 recettes par page
    page = request.GET.get('page')
    favorites = paginator.get_page(page)
    
    context = {
        'favorites': favorites,
        'title': 'Mes Favoris',
    }
    return render(request, 'recipes/favorites.html', context)

@login_required
def delete_recipe_image(request, image_id):
    image = get_object_or_404(RecipeImage, id=image_id)
    if image.recipe.author != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    image.delete()
    return JsonResponse({'success': True})
