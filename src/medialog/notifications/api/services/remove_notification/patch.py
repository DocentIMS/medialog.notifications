# -*- coding: utf-8 -*-
import logging

from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

logger = logging.getLogger(__name__)

# TO DO, should probably be 'PATCH'


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class RemoveNotification(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        result = {
            "remove_notification": {
                "@id": "{}/@remove_notification".format(
                    self.context.absolute_url(),
                ),
            },
        }

        if not expand:
            return result

        try:
            user_id = api.user.get_current().getId()
            notify_users = set(self.context.notify_users or [])
            if user_id and user_id in notify_users:
                notify_users.discard(user_id)
                self.context.notify_users = notify_users
                self.context.reindexObject()
            # TO DO: How can we refresh page
            return True
        except Exception:
            logger.exception("Failed to remove notification for current user")
            return False

        # return True


class RemoveNotificationGet(Service):

    def reply(self):
        service_factory = RemoveNotification(self.context, self.request)
        return service_factory(expand=True)["remove_notification"]
