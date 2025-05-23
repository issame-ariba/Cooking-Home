from django import template
from django.templatetags.static import static
from django.db.models import Avg
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.html import format_html

register = template.Library()

@register.filter
def average_rating(ratings):
    if not ratings:
        return 0
    avg = ratings.aggregate(Avg('value'))['value__avg']
    return round(avg, 1) if avg else 0

@register.filter
def get_image_url(recipe):
    """
    Retourne l'URL de la première image de la recette ou l'image par défaut si aucune image n'est disponible.
    """
    if recipe.images.exists():
        return recipe.images.first().image.url
    return static('images/default-recipe.jpg')

@register.simple_tag
def get_hero_image():
    """
    Retourne l'URL de l'image de la bannière hero.
    """
    return static('images/hero-banner.jpg')

@register.filter
def get_difficulty_color(difficulty):
    """
    Retourne la classe de couleur en fonction de la difficulté.
    """
    colors = {
        'facile': 'bg-success',
        'moyen': 'bg-warning',
        'difficile': 'bg-danger'
    }
    return colors.get(difficulty.lower(), 'bg-secondary')

@register.filter
def split(value, arg):
    """
    Divise une chaîne de caractères en utilisant le séparateur spécifié.
    """
    return value.split(arg) 