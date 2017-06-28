from Acquisition import aq_inner, aq_parent
from tx.tiles.interfaces import IPageTilesSettings
from tx.tiles.interfaces import ITilesSettings
from persistent.dict import PersistentDict
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements


class TilesSettings(object):
    """
    """
    implements(IPageTilesSettings, IPageTilesSettings)

    interfaces = []

    def __init__(self, context):
        self.context = context

        try:
            annotations = IAnnotations(self.context)
        except TypeError:
            # XXX for things like plone.app.event, traversers
            # are not adaptable so we need to look at the parent here
            self.context = aq_parent(context)
            annotations = IAnnotations(self.context)

        self._metadata = annotations.get('tx.tiles', None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations['tx.tiles'] = self._metadata

        ctx = aq_inner(context)
        rootctx = getToolByName(ctx, 'portal_url').getPortalObject()
        rootannotations = IAnnotations(rootctx)
        self._rootmetadata = rootannotations.get('tx.tiles', None)
        if self._rootmetadata is None:
            self._rootmetadata = PersistentDict()
            rootannotations['tx.tiles'] = self._rootmetadata

    @property
    def __parent__(self):
        return self.context

    @property
    def __roles__(self):
        return self.context.__roles__

    def __setattr__(self, name, value):
        if name[0] == '_' or name in ['context', 'interfaces']:
            self.__dict__[name] = value
        else:
            self._metadata[name] = value

    def __getattr__(self, name):
        value = self._metadata.get(name)
        if value is None:
            # first check to see if there are global settings
            if name in self._rootmetadata:
                return self._rootmetadata[name]
            else:
                # no global settings, check to see if there are defaults
                for interface in self.interfaces:
                    v = interface.get(name)
                    if v:
                        return v.default
        return value


class PageTilesSettings(TilesSettings):
    interfaces = [ITilesSettings, IPageTilesSettings]

    def __getattr__(self, name):
        if name == 'tiles':
            # somehow this default value gets manually set. This prevents this
            # form happening on the tiles...
            return self._metadata.get(name, [])
        return super(PageTilesSettings, self).__getattr__(name)

