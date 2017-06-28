from zope.interface import Interface, Attribute
from zope import schema
from tx.slider import message_factory as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from OFS.interfaces import IItem
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.namedfile import field

class ISliderLayer(Interface):
    """
    marker interface for slider layer
    """


class ISliderPage(Interface):
    """
    marker interface for a page that implements a slider
    """

class ISliderUtilProtected(Interface):

    def enable():
        """
        enable slider on this object
        """

    def disable():
        """
        disable slider on this object
        """


class ISliderUtil(Interface):

    def enabled_here():
        """
        checks if slider is enabled in context
        """

    def enabled():
        """
        checks if slider is enabled in aquisition chain
        """

    def should_include():
        """
        if the slider files should be included
        """

class ISlider(Interface):
    """Marker interface"""


class ISliderSettings(Interface):
    """
    The actual slider settings
    """

    configuration = schema.Choice(
        source="slider_configuration_choices",
        title=_(u"Slider configuration"),
        description=_(u"Choose a configuration. Configurations can be added in the control panel."),
        required=True
    )

    only_here = schema.Bool(
        title=_(u'Show only on this page'),
        description=_(u"If unchecked slider will be shown on subpages"),
        default=True,
        required=True
    )

    effect = schema.Choice(
        source="slider_effect_choices",
        title=_(u"Effect"),
        description=_(u"Leave on 'no choice' for default effect."),
        required=False
    )

    speed = schema.Int(
        title=_(u"Speed"),
        description=_(u"Speed at which the slides will transition (in milliseconds). '0' for Default."),
        default=0,
        required=False
    )

    pause = schema.Int(
        title=_(u"Pause"),
        description=_(u"Duration of the pause between transitions (in milliseconds). '0' for Default."),
        default=0,
        required=False
    )

    continuous = schema.Bool(
        title=_(u"Continuous"),
        description=_(u"Loop the slider continuously."),
        default=True
    )

    navigation_type = schema.Choice(
        source="slider_navigation_type_choices",
        title=_(u"Type of navigation"),
        description=_(u"Leave on 'no choice' for default navigation type."),
        required=False
    )

    randomize = schema.Bool(
        title=_(u"Randomize the slides"),
        default=False,
        required=False
    )


class IPageSliderSettings(Interface):
    """
    difference here is the user creates all his slides
    """
    
    show = schema.Bool(
        title=_(u"Show the slider"),
        description=_(u"Uncheck to hide the slider."),
        default=True,
        required=True
    )

    sliderposition = schema.Choice(
        title=_(u"Slider position"),
        default="portal_top",
        vocabulary=SimpleVocabulary([
            SimpleTerm(title=_(u"Portal top"),    value='portal_top'),
            SimpleTerm(title=_(u"Below title"),   value='below_content_title'),
            SimpleTerm(title=_(u"Below content"), value='below_content'),
        ]),
        required=True)

    slides = schema.List(
        title=_(u"Slides"),
        default=[]
    )


class ISlide(Interface):

    link_reference = schema.Choice(
        title=_(u"Link to content"),
        description=_(u"Choose a content item to link this slide to."),
        source=SearchableTextSourceBinder({},
                                          default_query='path:')
    )
    
    image = schema.Bytes(
        title=_(u"Image"),
        required=False
    )

    slide = schema.Text(
        title=_(u"Text"),
        required=False
    )

    index = schema.Int(
        title=u'',
        required=False
    )


class ISlidesContext(IItem):
    """
    Context to allow traversing to the slides list
    """


class ISlideContext(IItem):
    """
    Context to allow traversing to a slide on a ISlidesContext object
    """
    index = Attribute("""Index of the slide on the object""")
