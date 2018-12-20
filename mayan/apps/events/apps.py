from __future__ import unicode_literals

from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common import (
    MayanAppConfig, menu_list_facet, menu_object, menu_secondary,
    menu_tools, menu_topbar, menu_user
)
from mayan.apps.common.widgets import TwoStateWidget
from mayan.apps.navigation import SourceColumn

from .licenses import *  # NOQA
from .links import (
    link_current_user_events, link_event_types_subscriptions_list,
    link_events_list, link_notification_mark_read,
    link_notification_mark_read_all, link_user_events,
    link_user_notifications_list
)
from .widgets import event_object_link, event_type_link, event_user_link


class EventsApp(MayanAppConfig):
    app_namespace = 'events'
    app_url = 'events'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.events'
    verbose_name = _('Events')

    def ready(self):
        super(EventsApp, self).ready()
        Action = apps.get_model(app_label='actstream', model_name='Action')
        Notification = self.get_model(model_name='Notification')
        StoredEventType = self.get_model(model_name='StoredEventType')
        User = get_user_model()

        SourceColumn(
            source=Action, label=_('Timestamp'), attribute='timestamp'
        )
        SourceColumn(
            source=Action, label=_('Actor'),
            func=lambda context: event_user_link(context['object'])
        )
        SourceColumn(
            source=Action, label=_('Event'),
            func=lambda context: event_type_link(context['object'])
        )
        SourceColumn(
            source=Action, label=_('Action object'),
            func=lambda context: event_object_link(
                entry=context['object'], attribute='action_object'
            )
        )

        SourceColumn(
            source=StoredEventType, label=_('Namespace'), attribute='namespace'
        )
        SourceColumn(
            source=StoredEventType, label=_('Label'), attribute='label'
        )

        SourceColumn(
            source=Notification, label=_('Timestamp'),
            attribute='action.timestamp'
        )
        SourceColumn(
            source=Notification, label=_('Actor'), attribute='action.actor'
        )
        SourceColumn(
            source=Notification, label=_('Event'),
            func=lambda context: event_type_link(context['object'].action)
        )
        SourceColumn(
            source=Notification, label=_('Target'),
            func=lambda context: event_object_link(context['object'].action)
        )
        SourceColumn(
            source=Notification, label=_('Seen'),
            func=lambda context: TwoStateWidget(
                state=context['object'].read
            ).render()
        )

        menu_list_facet.bind_links(
            links=(link_user_events,), sources=(User,)
        )
        menu_object.bind_links(
            links=(link_notification_mark_read,), sources=(Notification,)
        )
        menu_secondary.bind_links(
            links=(link_notification_mark_read_all,),
            sources=('events:user_notifications_list',)
        )
        menu_tools.bind_links(links=(link_events_list,))
        menu_topbar.bind_links(
            links=(link_user_notifications_list,), position=1
        )
        menu_user.bind_links(
            links=(
                link_event_types_subscriptions_list, link_current_user_events
            )
        )
