from OFS.SimpleItem import SimpleItem
from zope.publisher.interfaces.browser import IBrowserPublisher
from tx.tiles.interfaces import ITileContext, ITilesContext
from zope.interface import implements
from zope.publisher.interfaces import NotFound

class TileContext(SimpleItem):
    """
    This is a transient item that allows us to traverse through (a wrapper of)
    a tile from a wrapper of a tiles list on an object
    """
    implements(ITileContext, IBrowserPublisher)

    def __init__(self, context, request, uuid):
        super(TileContext, self).__init__(context, request)
        self.context = context
        self.request = request
        self.uuid = uuid

    def publishTraverse(self, traverse, name):
        """ shouldn't go beyond this so just call the parent
        """
        return super(TileContext, self).publishTraverse(traverse, name)

    def browserDefault(self, request):
        """ Can't really traverse to anything else
        """
        raise NotFound(self, "The requested resource does not exist.")

    def absolute_url(self):
        return self.context.absolute_url()


class TilesContext(SimpleItem):
    """
    This is a transient item that allows us to traverse through (a wrapper of)
    a tiles list on an object
    """
    implements(ITilesContext, IBrowserPublisher)

    def __init__(self, context, request):
        super(TilesContext, self).__init__(context, request)

    def publishTraverse(self, traverse, uuid):
        """ 
        Look up the index whose name matches the next URL and wrap it.
        """
        return TileContext(self.context,
                            self.request,
                            uuid).__of__(self)

    def browserDefault(self, request):
        """ if nothing specified, just go to the regular tiles view
        """
        raise NotFound(self, "The requested resource does not exist.")

    def absolute_url(self):
        return self.context.absolute_url()
