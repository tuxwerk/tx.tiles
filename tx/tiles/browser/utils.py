from zope.interface import implements, alsoProvides, noLongerProvides
from Products.Five.browser import BrowserView
from tx.tiles.interfaces import ITilesUtilProtected, \
    ITilesPage, ITilesUtil
from Products.CMFCore.utils import getToolByName

from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from zope.component import getMultiAdapter
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.interfaces import ISiteRoot
from tx.tiles.settings import PageTilesSettings
import copy

class TilesUtilProtected(BrowserView):
    """
    a protected traverable utility for
    enabling and disabling tiless
    """
    implements(ITilesUtilProtected)

    def enable(self):
        utils = getToolByName(self.context, 'plone_utils')

        if ITilesPage.providedBy(self.context):
            self.request.response.redirect(self.context.absolute_url())
        else:            
            alsoProvides(self.context, ITilesPage)
            if getattr(self.context, 'getCanonical', None) is not None:
                canonical = self.context.getCanonical()
                if self.context != canonical and ITilesPage.providedBy(canonical):
                    # we copy the fields from the translation original
                    annotations = IAnnotations(canonical)
                    settings = copy.deepcopy(annotations.get('tx.tiles', {}))
                    settings['show'] = False
                    annotations_new = IAnnotations(self.context)
                    annotations_new['tx.tiles'] = settings
            self.context.reindexObject(idxs=['object_provides'])
            utils.addPortalMessage("Tiles added.")
            self.request.response.redirect('%s/@@tx-tiles-settings' % (
                self.context.absolute_url()))

    def disable(self):
        utils = getToolByName(self.context, 'plone_utils')

        if ITilesPage.providedBy(self.context):
            noLongerProvides(self.context, ITilesPage)
            self.context.reindexObject(idxs=['object_provides'])

            #now delete the annotation
            annotations = IAnnotations(self.context)
            metadata = annotations.get('tx.tiles', None)
            if metadata is not None:
                del annotations['tx.tiles']

            utils.addPortalMessage("Tiles removed.")

        self.request.response.redirect(self.context.absolute_url())


class TilesUtil(BrowserView):
    """
    a public traverable utility that checks if a
    tile is enabled
    """
    implements(ITilesUtil)

    def tilesobject(self):
        for item in self.context.aq_chain:
            if ITilesPage.providedBy(item):
                return item
            if ISiteRoot.providedBy(item):
                return None

    def enabled_here(self):
        return ITilesPage.providedBy(self.context)
    
    def enabled(self):
        tilesobject = self.tilesobject()
        if tilesobject:
            if tilesobject != self.context:
                if PageTilesSettings(tilesobject).only_here:
                    return False
            return True
        else:
            return False

    def should_include(self):
        return self.enabled()

