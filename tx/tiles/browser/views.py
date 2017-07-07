from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.ATContentTypes.interface.topic import IATTopic
from Products.ATContentTypes.interface.folder import IATFolder, IATBTreeFolder

from tx.tiles.settings import PageTilesSettings
from zope.publisher.interfaces import NotFound
import time
from email.Utils import formatdate

try:
    from plone.app.collection.interfaces import ICollection
    from plone.app.querystring import queryparser
except ImportError:
    from zope.interface import Interface
    class ICollection(Interface):
        pass

class TileBaseView(BrowserView):

    def __init__(self, context, request):
        super(TileBaseView, self).__init__(context, request)
        self.settings = PageTilesSettings(context.context)
        self.tiles   = self.settings.tiles
    
    def _index_of_tile(self, uuid):
        for i, dic in enumerate(self.settings.tiles):
            if dic.get('uuid') == uuid:
                return i
        raise NotFound(self, "The requested resource does not exist.")

    
class TileImageView(TileBaseView):
    """
    Download a tile image
    """

    def __init__(self, context, request):
        super(TileImageView, self).__init__(context, request)

    def __call__(self):
        index = self._index_of_tile(self.context.uuid)

        if not self.tiles[index].get('image_type'):
            raise NotFound(self, "The requested resource does not exist.")

        response = self.request.response

        future = time.time() + 60*60*24*365
        response.setHeader('Expires',
                           formatdate(float(future), usegmt=True))
        response.setHeader('Content-Type',
                           u"image/" + self.tiles[index].get('image_type').lower())
        return self.tiles[index].get('image')

class RemoveTileView(TileBaseView):

    def __init__(self, context, request):
        super(RemoveTileView, self).__init__(context, request)

    def __call__(self):
        index = self._index_of_tile(self.context.uuid)
        del self.tiles[index]
        self.settings.tiles = self.tiles
        return 'ok'

class OrderTiles(TileBaseView):

    def __init__(self, context, request):
        super(OrderTiles, self).__init__(context, request)
        
    def __call__(self):
        order = [str(uuid) for uuid in self.request.get('order[]')]

        if len(order) != len(self.tiles):
            self.request.response.setStatus(status=403,
                                            reason="missing tiles")

        newtiles = []
        for index in order:
            newtiles.append(self.tiles[self._index_of_tile(index)])

        self.settings.tiles = newtiles
        return 'done'
