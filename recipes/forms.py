from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, UserProfile, Category, RecipeImage, RecipeComment, RecipeRating

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Prénom")
    last_name = forms.CharField(max_length=30, required=False, label="Nom")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name', 'bio', 'specialties', 'avatar', 'location', 'website', 'social_media')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'specialties': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'social_media': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class RecipeForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        help_text="Vous pouvez sélectionner plusieurs images"
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'preparation_time', 'cooking_time', 'servings', 'difficulty', 'category', 'tags', 'cover_image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 10}),
            'instructions': forms.Textarea(attrs={'rows': 10}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        ingredients = cleaned_data.get('ingredients')
        instructions = cleaned_data.get('instructions')
        preparation_time = cleaned_data.get('preparation_time')
        cooking_time = cleaned_data.get('cooking_time')
        servings = cleaned_data.get('servings')
        difficulty = cleaned_data.get('difficulty')
        category = cleaned_data.get('category')

        if not title:
            self.add_error('title', 'Le titre est requis')
        if not description:
            self.add_error('description', 'La description est requise')
        if not ingredients:
            self.add_error('ingredients', 'Les ingrédients sont requis')
        if not instructions:
            self.add_error('instructions', 'Les instructions sont requises')
        if not preparation_time:
            self.add_error('preparation_time', 'Le temps de préparation est requis')
        if not cooking_time:
            self.add_error('cooking_time', 'Le temps de cuisson est requis')
        if not servings:
            self.add_error('servings', 'Le nombre de portions est requis')
        if not difficulty:
            self.add_error('difficulty', 'La difficulté est requise')
        if not category:
            self.add_error('category', 'La catégorie est requise')

        return cleaned_data

class RatingForm(forms.Form):
    value = forms.IntegerField(min_value=1, max_value=5)

class RecipeSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control me-2',
            'placeholder': 'Rechercher une recette...',
            'aria-label': 'Rechercher'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'Toutes les difficultés')] + Recipe.DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    preparation_time = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Temps de préparation maximum (minutes)'
        })
    )

class RecipeCommentForm(forms.ModelForm):
    class Meta:
        model = RecipeComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Partagez votre avis sur cette recette...'
            })
        } 