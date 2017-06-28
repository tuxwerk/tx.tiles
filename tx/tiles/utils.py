from zope.component import getUtility
from plone.registry.interfaces import IRegistry

def slider_settings_css(settings):
    """
    defined here because then it can be used in the widget
    and view that use the same .pt
    """
    configs = getUtility(IRegistry)['tx.slider.configlet.ISliderControlPanelSchema.configuration']
    ratio = str( (400.0 / 1000.0) * 100 )
    for config in configs:
        c = config.split(":")
        if c[0] == settings.configuration:
            ratio = str( (float(c[3]) / float(c[2])) * 100 )
            
    return """
    #tx-slider-widget li.sortable-placeholder,
    #tx-slider-widget ul li {
        padding-bottom: %(height)s%%;
    }
    """ % {
        'height': ratio
    }
