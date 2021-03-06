from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.form.browser.textwidgets import IntWidget

#from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
try:
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
except ImportError:
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile


class HiddenWidget(IntWidget):

    def __call__(self):
        return self.hidden()


class TilesWidget(SimpleInputWidget):
    """
    this widget pretty much is the same as the Tiles view
    In itself, it does not provide any data manipulatation, but
    it does provide the correct urls to perform the editing action
    for each tile
    """

    template = ViewPageTemplateFile('browser/templates/tiles_widget.pt')

    def __init__(self, field, request):
        SimpleInputWidget.__init__(self, field, request)

        # field/settings/context
        self.tiles_url = self.context.context.context.absolute_url()
        self.portal_url = self.context.context.context.portal_url()
        # field/settings
        self.settings = self.context.context
        # since this uses the same .pt file
        self.tiles = self.settings.tiles

    def __call__(self):
        return self.template(self)

    def hasInput(self):
        """
        data should never change here....
        """
        return False
