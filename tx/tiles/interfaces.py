from zope.interface import Interface, Attribute
from zope import schema
from tx.tiles import message_factory as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from OFS.interfaces import IItem
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.namedfile import field

class ITilesLayer(Interface):
    """
    marker interface for tiles layer
    """


class ITilesPage(Interface):
    """
    marker interface for a page that implements tiles
    """

class ITilesUtilProtected(Interface):

    def enable():
        """
        enable tiles on this object
        """

    def disable():
        """
        disable tiles on this object
        """


class ITilesUtil(Interface):

    def enabled_here():
        """
        checks if tiles is enabled in context
        """

    def enabled():
        """
        checks if tiles is enabled in aquisition chain
        """

    def should_include():
        """
        if the tiles files should be included
        """

class ITiles(Interface):
    """Marker interface"""


class ITilesSettings(Interface):
    """
    The actual tiles settings
    """

    configuration = schema.Choice(
        source="tiles_configuration_choices",
        title=_(u"Tiles configuration"),
        description=_(u"Choose a configuration. Configurations can be added in the control panel."),
        required=True
    )

    only_here = schema.Bool(
        title=_(u'Show only on this page'),
        description=_(u"If unchecked tiles will be shown on subpages"),
        default=True,
        required=True
    )

class IPageTilesSettings(Interface):
    """
    difference here is the user creates all his tiles
    """
    
    show = schema.Bool(
        title=_(u"Show the tiles"),
        description=_(u"Uncheck to hide the tiles."),
        default=True,
        required=True
    )

    tilesposition = schema.Choice(
        title=_(u"Tiles position"),
        default="portal_top",
        vocabulary=SimpleVocabulary([
            SimpleTerm(title=_(u"Portal top"),    value='portal_top'),
            SimpleTerm(title=_(u"Below title"),   value='below_content_title'),
            SimpleTerm(title=_(u"Below content"), value='below_content'),
        ]),
        required=True)

    tiles = schema.List(
        title=_(u"Tiles"),
        default=[]
    )


class ITile(Interface):

    link_reference = schema.Choice(
        title=_(u"Link to content"),
        description=_(u"Choose a content item to link this tile to."),
        source=SearchableTextSourceBinder({},
                                          default_query='path:')
    )
    
    image = schema.Bytes(
        title=_(u"Image"),
        required=False
    )

    tile = schema.Text(
        title=_(u"Text"),
        required=False
    )

    index = schema.Int(
        title=u'',
        required=False
    )


class ITilesContext(IItem):
    """
    Context to allow traversing to the tiles list
    """


class ITileContext(IItem):
    """
    Context to allow traversing to a tile on a ITilesContext object
    """
    index = Attribute("""Index of the tile on the object""")
