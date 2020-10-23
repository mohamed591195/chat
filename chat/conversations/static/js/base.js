// ajax setup
function getCookie(name) {

    'use strict';

    var cookieValue = null,
        i,
        cookies,
        cookie;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = 0; i < cookies.length; i += 1) {
            cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {

    'use strict';
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {

        'use strict';

        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// end ajax setup

// nav-bar functionality
$('.avatar').on('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    $('#notifications-list').hide()
    $('#avatar-list').toggle()
})

$(document).on('click', () => {
    $('#avatar-list').hide()
    $('#notifications-list').hide()
})

$('.notifications-bill').on('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    $('#avatar-list').hide()
    $(this).removeClass('notify');
    $('#notifications-list').toggle()

    if (unseenNotificationsExists) {

        let lastNotificationId = $('#notifications-list > li').first().data('id');

        $.ajax({
            type: 'POST',
            url: setNotficationsSeenURL,
            data: {
                id: lastNotificationId,
                loadedNotificationsCount,
            },
            success: function () {
                unseenNotificationsExists = false;
            }
        })

    }
})

