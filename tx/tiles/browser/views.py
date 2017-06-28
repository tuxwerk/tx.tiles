from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.ATContentTypes.interface.topic import IATTopic
from Products.ATContentTypes.interface.folder import IATFolder, IATBTreeFolder

from tx.slider.settings import PageSliderSettings
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

class SlideBaseView(BrowserView):

    def __init__(self, context, request):
        super(SlideBaseView, self).__init__(context, request)
        self.settings = PageSliderSettings(context.context)
        self.slides   = self.settings.slides
    
    def _index_of_slide(self, uuid):
        for i, dic in enumerate(self.settings.slides):
            if dic.get('uuid') == uuid:
                return i
        raise NotFound(self, "The requested resource does not exist.")

    
class SlideImageView(SlideBaseView):
    """
    Download a slide image
    """

    def __init__(self, context, request):
        super(SlideImageView, self).__init__(context, request)

    def __call__(self):
        index = self._index_of_slide(self.context.uuid)

        if not self.slides[index].get('image_type'):
            raise NotFound(self, "The requested resource does not exist.")

        response = self.request.response

        future = time.time() + 60*60*24*365
        response.setHeader('Expires',
                           formatdate(float(future), usegmt=True))
        response.setHeader('Content-Type',
                           u"image/" + self.slides[index].get('image_type').lower())
        return self.slides[index].get('image')

class RemoveSlideView(SlideBaseView):
    """
    For doing operations on a slide
    """

    slides_template = ViewPageTemplateFile('templates/slides.pt')

    def __init__(self, context, request):
        super(RemoveSlideView, self).__init__(context, request)

    def __call__(self):
        index = self._index_of_slide(self.context.uuid)
        del self.slides[index]
        self.settings.slides = self.slides
        return 'ok'

class OrderSlides(SlideBaseView):

    def __init__(self, context, request):
        super(OrderSlides, self).__init__(context, request)
        
    def __call__(self):
        order = [str(uuid) for uuid in self.request.get('order[]')]

        if len(order) != len(self.slides):
            self.request.response.setStatus(status=403,
                                            reason="missing slides")

        newslides = []
        for index in order:
            newslides.append(self.slides[self._index_of_slide(index)])

        self.settings.slides = newslides
        return 'done'
