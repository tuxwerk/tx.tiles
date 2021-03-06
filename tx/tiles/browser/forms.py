from zope.formlib import form
from zope.interface import implements
from zope.component import adapts
import zope.lifecycleevent
from zope.component import getMultiAdapter
from uuid import uuid4
from plone.fieldsets.fieldsets import FormFieldsets
from plone.fieldsets.form import FieldsetsEditForm

from plone.scale.scale import scaleImage

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.app.form import base as ploneformbase
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#FIXME: add a nice widget for image upload
#from plone.app.form.widgets.image import ImageWidget

from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from five.formlib import formbase

from tx.tiles.interfaces import ITilesPage, ITile, IPageTilesSettings, ITilesSettings
from tx.tiles import message_factory as _
from tx.tiles.widgets import TilesWidget, HiddenWidget
from tx.tiles.settings import PageTilesSettings
from plone.app.form.validators import null_validator
from Products.statusmessages.interfaces import IStatusMessage

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

class AddTileAdapter(SchemaAdapterBase):
    """
    This is getting a little ugly....  Store index
    in the request.
    """
    adapts(ITilesPage)
    implements(ITile)

    def __init__(self, context):
        super(AddTileAdapter, self).__init__(context)

        self.settings = PageTilesSettings(context)
        self.request = context.REQUEST
        self.portal_catalog    = context.portal_catalog
        self.portal_url        = context.portal_url
        self.portal_properties = context.portal_properties

    def __get_property__(self, name):
        if self.index == -1:  # creating new
            return u""
        else:
            val = self.settings.tiles[self.index]
            if isinstance(val, basestring):
                return val
            elif isinstance(val, dict) and name in val:
                return val[name]
        return u""
        
    def get_tile(self):
        return self.__get_property__('html')

    def set_tile(self, value):
        pass

    def get_index(self):
        index = self.request.get('index', -1)
        if index != -1:
            for i, dic in enumerate(self.settings.tiles):
                if dic.get('uuid') == index:
                    index = i
        return index

    def set_index(self, value):
        pass

    def get_url(self):
        return self.__get_property__('url')

    def set_url(self, value):
        pass

    def get_configuration(self):
        return self.__get_property__('configuration')

    def set_configuration(self, value):
        pass

    def get_heading(self):
        return self.__get_property__('heading')

    def set_heading(self, value):
        pass

    def get_image(self):
        return self.__get_property__('image')

    def set_image(self, value):
        pass

    def get_link_reference(self):
        return self.__get_property__('link_reference')

    def set_link_reference(self, value):
        pass

    link_reference = property(get_link_reference, set_link_reference)
    url = property(get_url, set_url)
    configuration = property(get_configuration, set_configuration)
    heading = property(get_heading, set_heading)
    tile = property(get_tile, set_tile)
    index = property(get_index, set_index)
    image = property(get_image, set_image)

class AddTileForm(formbase.EditFormBase):
    """
    The add/edit form for a tile
    """
    form_fields = form.FormFields(ITile)
    form_fields['index'].custom_widget = HiddenWidget
    #form_fields['image'].custom_widget = ImageWidget
    form_fields['tile'].custom_widget = WYSIWYGWidget
    form_fields['link_reference'].custom_widget = UberSelectionWidget
    
    label = _(u"Edit tile")
    #description = _(u'description_add_tile_form', default=u"")
    form_name = _(u"Add/Update Tile")

    @form.action(_(u"Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(self.context))
            zope.event.notify(ploneformbase.EditSavedEvent(self.context))
            IStatusMessage(self.request).addStatusMessage(
                _("Changes saved."), type="info")
        else:
            zope.event.notify(ploneformbase.EditCancelledEvent(self.context))
            IStatusMessage(self.request).addStatusMessage(
                _("No changes made."), type="info")

        self.settings = PageTilesSettings(self.context)
        tiles = self.settings.tiles
        index = data.get('index', -1)

        image = data.get('image')
        image_type = None
        if image != None:
            scale_width = getUtility(IRegistry)['tx.tiles.configlet.ITilesControlPanel.image_scale_width']
            (image, image_type, image_size) = scaleImage(image, width=scale_width)
        else:
            if index != -1:
                image      = tiles[index].get('image')
                image_type = tiles[index].get('image_type')

        # create new uuid on each save
        uuid = uuid4().hex

        value = {
            'link_reference': data.get('link_reference'),
            'image': image,
            'image_type': image_type,
            'configuration': data.get('configuration'),
            'heading': data.get('heading'),
            'html': data.get('tile'),
            'url': data.get('url'),
            'uuid': uuid
        }

        if index == -1:
            tiles.append(value)
            index = len(tiles) - 1
        else:
            tiles[index] = value

        self.settings.tiles = tiles

        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')() + "/@@tx-tiles-settings"
        self.request.response.redirect(url)

    @form.action(_(u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_("Changes canceled."),
                                                      type="info")
 
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')() + "/@@tx-tiles-settings"
        self.request.response.redirect(url)
        return ''


class TilesPageSettingsForm(FieldsetsEditForm):
    """
    The page that holds all the tiles settings
    """
    tiles = FormFieldsets(IPageTilesSettings)
    tiles.id = 'tiles'
    tiles.label = _(u'Tiles')

    settings = FormFieldsets(ITilesSettings)
    settings.id = 'settings'
    settings.label = _(u'Settings')
    
    form_fields = FormFieldsets(tiles, settings)
    #our revised TilesWidget that only displays tiles really
    form_fields['tiles'].custom_widget = TilesWidget
    label = _(u"Edit Tiles")
