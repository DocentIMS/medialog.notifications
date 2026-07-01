# -*- coding: utf-8 -*-
from medialog.notifications.interfaces import IMedialogNotificationsLayer
from medialog.notifications.testing import MEDIALOG_NOTIFICATIONS_FUNCTIONAL_TESTING
from medialog.notifications.testing import MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        alsoProvides(self.portal.REQUEST, IMedialogNotificationsLayer)
        api.content.create(self.portal, "Folder", "other-folder")

    def test_remove_notification_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST),
            name="remove-notification",
        )
        self.assertTrue(view.__name__ == "remove-notification")


class ViewsFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_NOTIFICATIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
