# -*- coding: utf-8 -*-
from medialog.notifications.interfaces import IMedialogNotificationsLayer
from medialog.notifications.testing import MEDIALOG_NOTIFICATIONS_FUNCTIONAL_TESTING
from medialog.notifications.testing import MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        alsoProvides(self.portal.REQUEST, IMedialogNotificationsLayer)
        api.content.create(self.portal, "Notification", "my-notification")
        api.content.create(self.portal, "Document", "front-page")

    def test_notification_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal["my-notification"], self.portal.REQUEST),
            name="notification-view",
        )
        self.assertTrue(view.__name__ == "notification-view")

    def test_notification_view_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST),
                name="notification-view",
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
