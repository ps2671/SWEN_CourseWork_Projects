var notify_badge_id;
var notify_menu_id;
var notify_api_url;
var notify_fetch_count;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badge = document.getElementById(notify_badge_id);
    if (badge) {
        badge.innerHTML = data.unread_count;
    }
}

function fill_notification_list(data) {
    var menu = document.getElementById(notify_menu_id);
    if (menu) {
        menu.innerHTML = "";
        for (var i=0; i < data.all_list.length; i++) {
            // use closures to execute immediately in order to avoid problem of
            // moving var declarations to top of scope and therefore overwrite
            // item.id of all links to only the last one
            (function () {
                var item = data.all_list[i];
                var message = "";
                if (typeof item.message !== 'undefined'){
                    message = item.message;
                }
                var notifText = document.createTextNode(message);
                var notifLink = document.createElement("a");
                notifLink.appendChild(notifText);
                notifLink.href = "#";
                // using an ajax request in order to avoid reloading the page.
                // must append a trailing slash for the URL for POST requests
                notifLink.addEventListener("click",  function() {
                    $.ajax({
                        url: "/mark-as-read/" + item.id + "/",
                        type: "POST",
                        data: "",
                        success: function(response) {
                            fill_notification_list(response);
                            fill_notification_badge(response)
                        }
                    });
                });
                if (item.is_read == false) {
                    notifLink.className += "notif-unread"
                }

                var notifListItem = document.createElement("li");
                notifListItem.appendChild(notifLink);
                menu.appendChild(notifListItem);
            }());
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.onreadystatechange = function () {
            if (r.readyState != 4 || r.status != 200) {
                consecutive_misfires++;
            } else {
                consecutive_misfires = 0;
                for (var i=0; i < registered_functions.length; i++) {
                    var func = registered_functions[i];
                    func(JSON.parse(r.responseText));
                }
            }
        };
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data, notify_refresh_period);
    } else {
        var badge = document.getElementById(notify_badge_id);
        if (badge) {
            badge.innerHTML = "!";
            badge.title = "Connection lost!"
        }
    }
}

/*
 * Cookie and security code courtesy of: https://docs.djangoproject.com/en/1.9/ref/csrf/
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
setTimeout(fetch_api_data, 100);