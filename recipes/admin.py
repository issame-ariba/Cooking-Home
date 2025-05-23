from django.contrib import admin
from .models import Recipe, Category, RecipeRating, RecipeComment, UserProfile, RecipeImage

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'difficulty', 'created_at')
    list_filter = ('category', 'difficulty', 'created_at')
    search_fields = ('title', 'description', 'ingredients')
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(RecipeRating)
class RecipeRatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('recipe__title', 'user__username')

@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('recipe__title', 'user__username', 'content')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'location')
    search_fields = ('user__username', 'display_name', 'location')

@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('recipe__title',)
