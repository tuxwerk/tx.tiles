from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from tx.tiles.settings import PageTilesSettings
from tx.tiles.interfaces import ITilesPage
from tx.tiles.browser.base import AbstractTilesView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import ISiteRoot

class BaseTilesViewlet(ViewletBase):

    index = ViewPageTemplateFile('templates/viewlet.pt')
    
    @memoize
    def tilesobject(self):
        for item in self.context.aq_chain:
            if ITilesPage.providedBy(item):
                return item
            if ISiteRoot.providedBy(item):
                return None
    
    @memoize
    def get_settings(self):
        return PageTilesSettings(self.tilesobject())

    @memoize
    def registry(self, key):
        return getUtility(IRegistry)['tx.tiles.configlet.ITilesControlPanel.' + key]

    @memoize
    def configuration(self):
        #return self.settings.configuration
        configs = self.registry('configuration')
        for config in configs:
            t = config.split(":")
            if t[1] == self.settings.configuration:
                return t
        return configs[0].split(":")
    
    @memoize
    def show(self):
        tilesobject = self.tilesobject()
        if tilesobject:
            if tilesobject != self.context:
                if self.settings.only_here:
                    return False
            if len(self.settings.tiles) == 0:
                return False
            else:
                return self.settings.show
        else:
            return False

    @memoize
    def tilesposition(self):
        return self.settings.tilesposition

    @memoize
    def class_name(self):
        #return self.settings.configuration
        c = self.configuration()
        if c:
            return c[1]

    @memoize
    def ratio(self):
        c = self.configuration()
        if c:
            return c[2] + ":" + c[3]

    @property
    def tiles(self):
        return self.settings.tiles

    @memoize
    def absolute_url(self):
        return self.tilesobject().absolute_url()

    settings = property(get_settings)

class TilesPortalTop(BaseTilesViewlet):

    def is_enabled(self):
        return self.show() and self.tilesposition() == "portal_top"

    def render(self):
        if self.is_enabled():
            return super(TilesPortalTop, self).render()
        else:
            return ""

class TilesBelowContentTitle(BaseTilesViewlet):

    def is_enabled(self):
        return self.show() and self.tilesposition() == "below_content_title"

    def render(self):
        if self.is_enabled():
            return super(TilesBelowContentTitle, self).render()
        else:
            return ""
    
class TilesBelowContent(BaseTilesViewlet):

    def is_enabled(self):
        return self.show() and self.tilesposition() == "below_content"

    def render(self):
        if self.is_enabled():
            return super(TilesBelowContent, self).render()
        else:
            return ""
    
