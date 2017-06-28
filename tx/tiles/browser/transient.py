from OFS.SimpleItem import SimpleItem
from zope.publisher.interfaces.browser import IBrowserPublisher
from tx.slider.interfaces import ISlideContext, ISlidesContext
from zope.interface import implements
from zope.publisher.interfaces import NotFound

class SlideContext(SimpleItem):
    """
    This is a transient item that allows us to traverse through (a wrapper of)
    a slide from a wrapper of a slides list on an object
    """
    implements(ISlideContext, IBrowserPublisher)

    def __init__(self, context, request, uuid):
        super(SlideContext, self).__init__(context, request)
        self.context = context
        self.request = request
        self.uuid = uuid

    def publishTraverse(self, traverse, name):
        """ shouldn't go beyond this so just call the parent
        """
        return super(SlideContext, self).publishTraverse(traverse, name)

    def browserDefault(self, request):
        """ Can't really traverse to anything else
        """
        raise NotFound(self, "The requested resource does not exist.")

    def absolute_url(self):
        return self.context.absolute_url()


class SlidesContext(SimpleItem):
    """
    This is a transient item that allows us to traverse through (a wrapper of)
    a slides list on an object
    """
    implements(ISlidesContext, IBrowserPublisher)

    def __init__(self, context, request):
        super(SlidesContext, self).__init__(context, request)

    def publishTraverse(self, traverse, uuid):
        """ 
        Look up the index whose name matches the next URL and wrap it.
        """
        return SlideContext(self.context,
                            self.request,
                            uuid).__of__(self)

    def browserDefault(self, request):
        """ if nothing specified, just go to the regular slides view
        """
        raise NotFound(self, "The requested resource does not exist.")

    def absolute_url(self):
        return self.context.absolute_url()
