// Fonction pour ajuster les quantités des ingrédients
function adjustIngredients(ingredients, ratio) {
    // Cette fonction sera implémentée plus tard pour gérer l'ajustement des quantités
    return ingredients;
}

// Gestion des favoris
function toggleFavorite(recipeId) {
    $.ajax({
        url: '/recipe/' + recipeId + '/favorite/',
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function(data) {
            if (data.success) {
                const btn = $(`[data-recipe-id="${recipeId}"]`);
                const icon = btn.find('i');
                icon.toggleClass('fas far');
            }
        }
    });
}

// Gestion des notes
function submitRating(recipeId, value) {
    $.ajax({
        url: '/recipe/' + recipeId + '/rate/',
        method: 'POST',
        data: { value: value },
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function(data) {
            if (data.success) {
                // Mettre à jour l'affichage de la note moyenne
                updateAverageRating(data.avg_rating);
            }
        }
    });
}

function updateAverageRating(avgRating) {
    const stars = $('.average-rating i');
    stars.each(function(index) {
        if (index < Math.floor(avgRating)) {
            $(this).removeClass('far').addClass('fas');
        } else {
            $(this).removeClass('fas').addClass('far');
        }
    });
}

// Prévisualisation des images
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = $('<img>').attr({
                'src': e.target.result,
                'class': 'img-thumbnail',
                'style': 'max-height: 200px;'
            });
            $('.img-thumbnail').remove();
            $(input).after(preview);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Initialisation des événements
$(document).ready(function() {
    // Gestion des favoris
    $('.favorite-btn').click(function() {
        const recipeId = $(this).data('recipe-id');
        toggleFavorite(recipeId);
    });

    // Gestion des notes
    $('.rating input').change(function() {
        const recipeId = $(this).closest('form').data('recipe-id');
        const value = $(this).val();
        submitRating(recipeId, value);
    });

    // Prévisualisation des images
    $('#id_image').change(function() {
        previewImage(this);
    });

    // Gestion des portions
    $('#servings').change(function() {
        const newServings = $(this).val();
        const originalServings = $(this).data('original-servings');
        const ratio = newServings / originalServings;
        
        $.ajax({
            url: $(this).data('adjust-url'),
            data: { servings: newServings },
            success: function(data) {
                if (data.success) {
                    $('#ingredients-list').html(data.adjusted_ingredients);
                }
            }
        });
    });

    // Initialisation des tooltips Bootstrap
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Gestion de la recherche en temps réel
    let searchTimeout;
    $('#recipe-search').on('input', function() {
        clearTimeout(searchTimeout);
        const query = $(this).val();
        
        searchTimeout = setTimeout(function() {
            $.get('/search/', { query: query }, function(data) {
                $('#search-results').html(data);
            });
        }, 300);
    });
}); 