from zope.component import getUtility
from plone.registry.interfaces import IRegistry

def tiles_settings_css(settings):
    """
    defined here because then it can be used in the widget
    and view that use the same .pt
    """
    configs = getUtility(IRegistry)['tx.tiles.configlet.ITilesControlPanelSchema.configuration']
    ratio = str( (400.0 / 1000.0) * 100 )
    for config in configs:
        c = config.split(":")
        if c[0] == settings.configuration:
            ratio = str( (float(c[3]) / float(c[2])) * 100 )
            
    return """
    #tx-tiles-widget li.sortable-placeholder,
    #tx-tiles-widget ul li {
        padding-bottom: %(height)s%%;
    }
    """ % {
        'height': ratio
    }
