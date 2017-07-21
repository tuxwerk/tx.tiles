#import unittest2 as unittest
import unittest
from tx.tiles.tests import BaseTest
from zope.component import getUtilitiesFor, queryUtility
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage


class TestSetup(BaseTest):
    """
    """

    def test_css_registry(self):
        pcss = self.portal.portal_css
        self.failUnless('++resource++tx-tiles-settings.css' in
                        [css.getId() for css in pcss.getResources()])
        self.failUnless('++resource++tx-tiles-viewlet.css' in
                        [css.getId() for css in pcss.getResources()])

    def test_css_registry_uninstalls(self):
        self.uninstall()
        pcss = self.portal.portal_css
        self.failUnless('++resource++tx-tiles-settings.css' not in
                        [css.getId() for css in pcss.getResources()])
        self.failUnless('++resource++tx-tiles-viewlet.css' not in
                        [css.getId() for css in pcss.getResources()])

    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++tx-tiles-settings.js' in
                        [js.getId() for js in pjavascripts.getResources()])

    def test_js_uninstalls(self):
        self.uninstall()
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++tx-tiles-settings.js' not in
                        [js.getId() for js in pjavascripts.getResources()])

    def test_actions_install(self):
        actionTool = self.portal.portal_actions
        #these would throw an exception if they weren't there..
        actionTool.getActionInfo(['object_buttons/enable_tiles'])
        actionTool.getActionInfo(['object_buttons/disable_tiles'])
        actionTool.getActionInfo(['object/tiles_settings'])

    def test_actions_uninstall(self):
        self.uninstall()
        actionTool = self.portal.portal_actions
        ob = actionTool['object_buttons']
        o = actionTool['object']
        #these would throw an exception if they weren't there..
        self.failUnless('enable_tiles' not in ob.objectIds())
        self.failUnless('disable_tiles' not in ob.objectIds())
        self.failUnless('tiles_settings' not in o.objectIds())

    def test_viewlet_installs(self):
        storage = queryUtility(IViewletSettingsStorage)
        self.failUnless('tx.tiles.portaltop' in
                        storage.getOrder('plone.portaltop', None))
        self.failUnless('tx.tiles.belowcontenttitle' in
                        storage.getOrder('plone.belowcontenttitle', None))
        self.failUnless('tx.tiles.belowcontent' in
                        storage.getOrder('plone.belowcontent', None))

    def test_viewlet_uninstalls(self):
        self.uninstall()
        storage = queryUtility(IViewletSettingsStorage)
        self.failUnless('tx.tiles.portaltop' not in
                        storage.getOrder('plone.portaltop', None))
        self.failUnless('tx.tiles.belowcontenttitle' not in
                        storage.getOrder('plone.belowcontenttitle', None))
        self.failUnless('tx.tiles.belowcontent' not in
                        storage.getOrder('plone.belowcontent', None))

    def test_permissions(self):
        """Ensure Site Administrators can manage tiless on Plone 4.1+."""
        mtool = getToolByName(self.portal, 'portal_membership', None)
        perm = 'tx.tiles: Manage tiles settings'
        roles = self.portal.rolesOfPermission
        if mtool and 'Site Administrator' in mtool.getPortalRoles():
            roles = [r['name'] for r in roles(perm) if r['selected']]
            self.assertEqual(roles, ['Site Administrator'])
        # FIXME: test permissions for editors

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
