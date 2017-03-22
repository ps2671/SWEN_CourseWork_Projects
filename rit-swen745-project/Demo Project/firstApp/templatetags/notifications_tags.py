# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.html import format_html

register = Library()


@register.assignment_tag(takes_context=True)
def notifications_unread(context):
    user = user_context(context)
    if not user:
        return ''
    return user.notifications.unread().count()


# Requires vanilla-js framework - http://vanilla-js.com/
@register.simple_tag
def register_notify_callbacks(badge_id='live_notify_badge',
                              menu_id='live_notify_list',
                              refresh_period=15,
                              callbacks='',
                              api_name='list',
                              fetch=10):
    refresh_period = int(refresh_period)*1000

    if api_name == 'list':
        api_url = reverse('live_all_notification_list')
    elif api_name == 'count':
        api_url = reverse('live_unread_notification_count')
    else:
        return ""
    definitions = """
        notify_badge_id='{badge_id}';
        notify_menu_id='{menu_id}';
        notify_api_url='{api_url}';
        notify_fetch_count='{fetch_count}';
        notify_refresh_period={refresh};
    """.format(
        badge_id=badge_id,
        menu_id=menu_id,
        api_url=api_url,
        fetch_count=fetch,
        refresh=refresh_period
    )

    script = "<script>"+definitions
    for callback in callbacks.split(','):
        script += "register_notifier("+callback+");"
    script += "</script>"
    return format_html(script)


@register.simple_tag(takes_context=True)
def live_notify_badge(context, badge_id='live_notify_badge', classes=""):
    user = user_context(context)
    if not user:
        return ''

    html = "<span id='{badge_id}' class='{classes}'>{unread}</span>".format(
        badge_id=badge_id, classes=classes, unread=user.notifications.unread().count()
    )
    return format_html(html)


@register.simple_tag(takes_context=True)
def live_notify_list(context, list_id='live_notify_list', classes=""):
    user = user_context(context)
    if not user:
        return ''

    html = "<ul id='{list_id}' class='{classes}'></ul>".format(list_id=list_id, classes=classes)
    return format_html(html)


def user_context(context):
    if 'user' not in context:
        return None

    user = context['user']
    if user.is_anonymous():
        return None
    return user
