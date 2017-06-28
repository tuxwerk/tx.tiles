from Products.CMFCore.utils import getToolByName
from tx.tiles.testing import \
    Tiles_INTEGRATION_TESTING, \
    Tiles_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
import unittest
from plone.app.testing import TEST_USER_ID
from tx.tiles.interfaces import ITilesLayer
from zope.interface import alsoProvides


class BaseTest(unittest.TestCase):

    layer = Tiles_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.app = self.layer['app']
        alsoProvides(self.request, ITilesLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def tearDown(self):
        pass

    def uninstall(self):
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(
            'profile-tx.tiles:uninstall')

    def create_object(self, id, type_name, parent=None):
        if parent:
            return parent[parent.invokeFactory(type_name=type_name, id=id)]
        else:
            return self.portal[self.portal.invokeFactory(
                type_name=type_name, id=id)]


class BaseFunctionalTest(BaseTest):
    layer = Tiles_FUNCTIONAL_TESTING
