import os
import requests
from PIL import Image
from io import BytesIO

def download_and_optimize_image(url, output_path, target_width=None):
    """
    Télécharge une image depuis une URL et l'optimise pour le web.
    """
    # Créer le dossier de destination s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Télécharger l'image
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    # Convertir en RGB si nécessaire
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Redimensionner si une largeur cible est spécifiée
    if target_width:
        ratio = target_width / img.width
        target_height = int(img.height * ratio)
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Optimiser et sauvegarder
    img.save(output_path, 'JPEG', quality=85, optimize=True)

def main():
    # URLs des images (remplacer par les URLs réelles)
    hero_image_url = "https://images.unsplash.com/photo-1556911220-e15b29be8c8f"
    default_recipe_url = "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
    
    # Chemins de sortie
    hero_output = "static/images/hero-banner.jpg"
    default_output = "static/images/default-recipe.jpg"
    
    # Télécharger et optimiser les images
    print("Téléchargement de l'image hero...")
    download_and_optimize_image(hero_image_url, hero_output, target_width=1920)
    
    print("Téléchargement de l'image par défaut...")
    download_and_optimize_image(default_recipe_url, default_output, target_width=800)
    
    print("Images téléchargées et optimisées avec succès!")

if __name__ == "__main__":
    main() 