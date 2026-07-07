# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from plone.protect.utils import safeWrite
import transaction


class IRemoveNotification(Interface):
    """Marker Interface for IRemoveNotification"""


class RemoveNotification(BrowserView):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self):
        # context = self.context
        user = api.user.get_current()
        user_id = user.getId()
        item = self.request.get("item")
        obj = api.content.get(UID=item) if item else None

        # Guard against a missing/invalid UID (endpoint is reachable by any
        # user, so a bad ``item`` must not raise an AttributeError / 500).
        if obj is not None and user_id:
            assigned = getattr(obj, "notification_assigned", None) or []
            if user_id in assigned:
                safeWrite(obj, self.request)
                readerlist = [uid for uid in assigned if uid != user_id]
                obj.notification_assigned = readerlist
                # if [] the notefication content is kept
                # maybe it should be hidden instead ?
                obj.reindexObject("notification_assigned")

        # Only redirect back to a same-origin referer to avoid an open
        # redirect; otherwise fall back to the portal root.
        referer = self.request.get_header("referer")
        portal_url = api.portal.get().absolute_url()
        if not referer or not referer.startswith(portal_url):
            referer = portal_url
        self.request.response.redirect(referer)
        # return True
