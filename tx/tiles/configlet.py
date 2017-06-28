from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts

from zope import schema
#from zope.formlib import form

from tx.tiles import message_factory as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.controlpanel.form import ControlPanelForm

from zope.component.hooks import getSite
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

def configuration_choices(context):
    configs = getUtility(IRegistry)['tx.tiles.configlet.ITilesControlPanelSchema.configuration']
    items = ()
    for config in configs:
        t = config.split(":")[0]
        items = ((t,t),) + items
    return SimpleVocabulary.fromItems(items)

class ITilesControlPanelSchema(Interface):
    """
    The actual tiles settings
    """

    configuration = schema.List(
        title=_(u'Configuration'),
        description=_(u"Enter one configuration per line. Format: 'Name:css-class-name:width:height'. css-class-name will be prefixed with 'tx-tiles-'. Uploaded images will be scaled down to width."),
        value_type=schema.TextLine(),
        required=True
    )

class ControlPanelForm(RegistryEditForm):

    form.extends(RegistryEditForm)
    schema = ITilesControlPanelSchema
    label = _(u"Tiles default settings")
    description = _(u'Default settings to use for all tiles.')
    
class ControlPanel(ControlPanelFormWrapper):

    form = ControlPanelForm
