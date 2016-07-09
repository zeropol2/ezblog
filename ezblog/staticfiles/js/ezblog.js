function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $modal = $('#delete-comfirm-modal')
        .on('shown.bs.modal', function(e) {
            $this = $(this);
        });
    $modal
        .find('.btn-modal-submit').on('click', function(e) {
            e.preventDefault();
            $.ajax({
                method: 'DELETE',
                url: $modal.data('href'),
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                },
            }).done(function(data) {
                window.location = $modal.data('next-to');
            }).fail(function(data) {
                alert(data);
            });
            return false;
        });

    $('.delete-post').on('click', function(e) {
        e.preventDefault();
        $this = $(this);
        $modal
            .data('href', $this.attr('href'))
            .data('next-to', $this.attr('data-next-to'));

        $modal.modal();

        return false;
    });
});


$(document).ready(function() {
    $('.update-post').on('click', function(e) {
        e.preventDefault();
        $this = $(this);
        if($('#edit-post-form').parsley().isValid()) {
            $.ajax({
                method: 'PUT',
                url: $this.attr('href'),
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                },
                data : $('#edit-post-form').serialize()
            }).done(function(data) {
                window.location = $this.attr('data-next-to');
            }).fail(function(data) {
                alert(data);
            });
        } else {
            $('#edit-post-form').parsley().validate()
        }
        return false;
    });
});


$(function () {
    $('#edit-post-form').parsley().on('field:validated', function() {
        var ok = $('.parsley-error').length === 0;
        $('.bs-callout-info').toggleClass('hidden', !ok);
        $('.bs-callout-warning').toggleClass('hidden', ok);
    })
});
