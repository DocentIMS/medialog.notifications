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
        api.content.create(self.portal, "Document", "front-page")

    def test_email_notification_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name="email-notification-view",
        )
        self.assertTrue(view.__name__ == "email-notification-view")

    def test_email_notification_view_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST),
                name="email-notification-view",
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
