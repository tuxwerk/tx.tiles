from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from tx.slider.settings import PageSliderSettings
from tx.slider.interfaces import ISliderPage
from tx.slider.browser.base import AbstractSliderView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import ISiteRoot

class BaseSliderViewlet(ViewletBase):

    index = ViewPageTemplateFile('templates/viewlet.pt')
    
    @memoize
    def sliderobject(self):
        for item in self.context.aq_chain:
            if ISliderPage.providedBy(item):
                return item
            if ISiteRoot.providedBy(item):
                return None
    
    @memoize
    def get_settings(self):
        return PageSliderSettings(self.sliderobject())

    @memoize
    def registry(self, key):
        return getUtility(IRegistry)['tx.slider.configlet.ISliderControlPanelSchema.' + key]

    @memoize
    def configuration(self):
        configs = self.registry('configuration')
        for config in configs:
            t = config.split(":")
            if t[0] == self.settings.configuration:
                return t
    
    @memoize
    def show(self):
        sliderobject = self.sliderobject()
        if sliderobject:
            if sliderobject != self.context:
                if self.settings.only_here:
                    return False
            if len(self.settings.slides) == 0:
                return False
            else:
                return self.settings.show
        else:
            return False

    @memoize
    def sliderposition(self):
        return self.settings.sliderposition

    @memoize
    def class_name(self):
        c = self.configuration()
        if c:
            return c[1]
        return "default"

    @memoize
    def ratio(self):
        c = self.configuration()
        if c:
            return c[2] + ":" + c[3]
        return "1000:400"

    @memoize
    def padding(self):
        c = self.configuration()
        if c:
            return str( (float(c[3]) / float(c[2])) * 100 )
        return str( (400.0 / 1000.0) * 100 )
                
    @memoize
    def effect(self):
        return self.settings.effect or self.registry('effect')
                
    @memoize
    def randomize(self):
        return self.settings.randomize

    @memoize
    def speed(self):
        return self.settings.speed or self.registry('speed')

    @memoize
    def pause(self):
        return self.settings.pause or self.registry('pause')

    @memoize
    def continuous(self):
        return self.settings.continuous

    @property
    def slides(self):
        return self.settings.slides

    @memoize
    def absolute_url(self):
        return self.sliderobject().absolute_url()

    @memoize
    def navigation_type(self):
    	return self.settings.navigation_type or self.registry('navigation_type')

    settings = property(get_settings)

class SliderPortalTop(BaseSliderViewlet):

    def is_enabled(self):
        return self.show() and self.sliderposition() == "portal_top"

    def render(self):
        if self.is_enabled():
            return super(SliderPortalTop, self).render()
        else:
            return ""

class SliderBelowContentTitle(BaseSliderViewlet):

    def is_enabled(self):
        return self.show() and self.sliderposition() == "below_content_title"

    def render(self):
        if self.is_enabled():
            return super(SliderBelowContentTitle, self).render()
        else:
            return ""
    
class SliderBelowContent(BaseSliderViewlet):

    def is_enabled(self):
        return self.show() and self.sliderposition() == "below_content"

    def render(self):
        if self.is_enabled():
            return super(SliderBelowContent, self).render()
        else:
            return ""
    
class SliderHead(BaseSliderViewlet, AbstractSliderView):

    index = ViewPageTemplateFile('templates/headviewlet.pt')

    def is_enabled(self):
        return self.show()

    def render(self):
        if self.is_enabled():
            return super(SliderHead, self).render()
        else:
            return ""
