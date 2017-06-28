from zope.interface import implements, alsoProvides, noLongerProvides
from Products.Five.browser import BrowserView
from tx.slider.interfaces import ISliderUtilProtected, \
    ISliderPage, ISliderUtil
from Products.CMFCore.utils import getToolByName

from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet
from zope.component import getMultiAdapter
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.interfaces import ISiteRoot
from tx.slider.settings import PageSliderSettings

class SliderUtilProtected(BrowserView):
    """
    a protected traverable utility for
    enabling and disabling sliders
    """
    implements(ISliderUtilProtected)

    def enable(self):
        utils = getToolByName(self.context, 'plone_utils')

        if ISliderPage.providedBy(self.context):
            self.request.response.redirect(self.context.absolute_url())
        else:            
            alsoProvides(self.context, ISliderPage)
            self.context.reindexObject(idxs=['object_provides'])
            utils.addPortalMessage("Slider added.")
            self.request.response.redirect('%s/@@tx-slider-settings' % (
                self.context.absolute_url()))

    def disable(self):
        utils = getToolByName(self.context, 'plone_utils')

        if ISliderPage.providedBy(self.context):
            noLongerProvides(self.context, ISliderPage)
            self.context.reindexObject(idxs=['object_provides'])

            #now delete the annotation
            annotations = IAnnotations(self.context)
            metadata = annotations.get('tx.slider', None)
            if metadata is not None:
                del annotations['tx.slider']

            utils.addPortalMessage("Slider removed.")

        self.request.response.redirect(self.context.absolute_url())


class SliderUtil(BrowserView):
    """
    a public traverable utility that checks if a
    slide is enabled
    """
    implements(ISliderUtil)

    def sliderobject(self):
        for item in self.context.aq_chain:
            if ISliderPage.providedBy(item):
                return item
            if ISiteRoot.providedBy(item):
                return None

    def enabled_here(self):
        return ISliderPage.providedBy(self.context)
    
    def enabled(self):
        sliderobject = self.sliderobject()
        if sliderobject:
            if sliderobject != self.context:
                if PageSliderSettings(sliderobject).only_here:
                    return False
            return True
        else:
            return False

    def should_include(self):
        return self.enabled()

