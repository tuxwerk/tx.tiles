from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig
from plone.testing import z2


class Tiles(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import tx.tiles
        xmlconfig.file('configure.zcml', tx.tiles,
                       context=configurationContext)
        z2.installProduct(app, 'tx.tiles')

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'tx.tiles:default')
        setRoles(portal, TEST_USER_ID, ('Member', 'Manager'))
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('plone_workflow')


Tiles_FIXTURE = Tiles()
Tiles_INTEGRATION_TESTING = IntegrationTesting(
    bases=(Tiles_FIXTURE,), name="Tiles:Integration")
Tiles_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(Tiles_FIXTURE,), name="Tiles:Functional")


def browserLogin(portal, browser, username=None, password=None):
    handleErrors = browser.handleErrors
    try:
        browser.handleErrors = False
        browser.open(portal.absolute_url() + '/login_form')
        if username is None:
            username = TEST_USER_NAME
        if password is None:
            password = TEST_USER_PASSWORD
        browser.getControl(name='__ac_name').value = username
        browser.getControl(name='__ac_password').value = password
        browser.getControl(name='submit').click()
    finally:
        browser.handleErrors = handleErrors


def createObject(context, _type, id, delete_first=True,
                 check_for_first=False, **kwargs):
    if delete_first and id in context.objectIds():
        context.manage_delObjects([id])
    if not check_for_first or id not in context.objectIds():
        return context[context.invokeFactory(_type, id, **kwargs)]

    return context[id]
