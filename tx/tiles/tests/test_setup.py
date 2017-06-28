import unittest2 as unittest
from tx.slider.tests import BaseTest
from zope.component import getUtilitiesFor, queryUtility
from Products.CMFCore.utils import getToolByName
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage


class TestSetup(BaseTest):
    """
    """

    def test_css_registry(self):
        pcss = self.portal.portal_css
        self.failUnless('++resource++easySlider.css' in
                        [css.getId() for css in pcss.getResources()])
        self.failUnless('++resource++slider-settings.css' in
                        [css.getId() for css in pcss.getResources()])

    def test_css_registry_uninstalls(self):
        self.uninstall()
        pcss = self.portal.portal_css
        self.failUnless('++resource++easySlider.css' not in
                        [css.getId() for css in pcss.getResources()])
        self.failUnless('++resource++slider-settings.css' not in
                        [css.getId() for css in pcss.getResources()])

    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++easySlider.js' in
                        [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++slider-settings.js' in
                        [js.getId() for js in pjavascripts.getResources()])

    def test_js_uninstalls(self):
        self.uninstall()
        pjavascripts = getToolByName(self.portal, 'portal_javascripts')
        self.failUnless('++resource++easySlider.js' not in
                        [js.getId() for js in pjavascripts.getResources()])
        self.failUnless('++resource++slider-settings.js' not in
                        [js.getId() for js in pjavascripts.getResources()])

    def test_actions_install(self):
        actionTool = self.portal.portal_actions

        #these would throw an exception if they weren't there..
        actionTool.getActionInfo(['object_buttons/enable_slider'])
        actionTool.getActionInfo(['object_buttons/disable_slider'])
        actionTool.getActionInfo(['object/slider_settings'])
        actionTool.getActionInfo(['object/view_slider_settings'])

    def test_actions_uninstall(self):
        self.uninstall()
        actionTool = self.portal.portal_actions

        ob = actionTool['object_buttons']
        os = actionTool['object']
        #these would throw an exception if they weren't there..
        self.failUnless('enable_slider' not in ob.objectIds())
        self.failUnless('disable_slider' not in ob.objectIds())
        self.failUnless('slider_settings' not in os.objectIds())
        self.failUnless('view_slider_settings' not in os.objectIds())

    def test_viewlet_installs(self):
        storage = queryUtility(IViewletSettingsStorage)
        self.failUnless('tx.slider' in
                        storage.getOrder('plone.belowcontenttitle', None))
        self.failUnless('tx.slider.head' in
                        storage.getOrder('plone.htmlhead.links', None))
        self.failUnless('tx.slider' in
                        storage.getOrder('plone.belowcontent', None))

    def test_viewlet_uninstalls(self):
        self.uninstall()
        storage = queryUtility(IViewletSettingsStorage)
        self.failUnless('tx.slider' not in
                        storage.getOrder('plone.belowcontenttitle', None))
        self.failUnless('tx.slider.head' not in
                        storage.getOrder('plone.htmlhead.links', None))
        self.failUnless('tx.slider' not in
                        storage.getOrder('plone.belowcontent', None))

    def test_permissions(self):
        """Ensure Site Administrators can manage sliders on Plone 4.1+."""
        mtool = getToolByName(self.portal, 'portal_membership', None)
        perm = 'tx.slider: Manage slider settings'
        roles = self.portal.rolesOfPermission
        if mtool and 'Site Administrator' in mtool.getPortalRoles():
            roles = [r['name'] for r in roles(perm) if r['selected']]
            self.assertEqual(roles, ['Site Administrator'])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
