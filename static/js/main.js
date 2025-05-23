$(document).ready(function() {
    // Gestion des favoris
    $('.favorite-btn').click(function(e) {
        e.preventDefault();
        const btn = $(this);
        const url = btn.data('url');
        
        $.post(url, {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        })
        .done(function(response) {
            if (response.is_favorite) {
                btn.html('<i class="fas fa-heart"></i>');
                btn.addClass('text-danger');
            } else {
                btn.html('<i class="far fa-heart"></i>');
                btn.removeClass('text-danger');
            }
        })
        .fail(function() {
            alert('Une erreur est survenue. Veuillez réessayer.');
        });
    });

    // Système de notation
    $('.rating-form').submit(function(e) {
        e.preventDefault();
        const form = $(this);
        const url = form.attr('action');
        
        $.post(url, form.serialize())
        .done(function(response) {
            $('.average-rating').text(response.average_rating.toFixed(1));
            $('.rating-count').text(response.rating_count);
        })
        .fail(function() {
            alert('Une erreur est survenue. Veuillez réessayer.');
        });
    });

    // Ajustement des portions
    $('#servings-adjust').on('input', function() {
        const ratio = $(this).val() / $(this).data('original');
        $('.ingredient-quantity').each(function() {
            const original = $(this).data('original');
            const adjusted = (original * ratio).toFixed(1);
            $(this).text(adjusted);
        });
    });

    // Validation du formulaire de recette
    $('#recipe-form').submit(function(e) {
        const requiredFields = ['title', 'description', 'ingredients', 'instructions'];
        let isValid = true;

        requiredFields.forEach(field => {
            const input = $(`#id_${field}`);
            if (!input.val().trim()) {
                isValid = false;
                input.addClass('is-invalid');
            } else {
                input.removeClass('is-invalid');
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Veuillez remplir tous les champs obligatoires.');
        }
    });

    // Prévisualisation de l'image
    $('#id_image').change(function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('.recipe-image-preview').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    // Animation du scroll
    $('a[href^="#"]').click(function(e) {
        e.preventDefault();
        const target = $(this.hash);
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });

    // Tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Confirmation de suppression
    $('.delete-confirm').click(function(e) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
            e.preventDefault();
        }
    });
}); 