from plone.memoize.view import memoize


class AbstractSliderView(object):
    """
    must have settings attribute specified
    """

    @property
    @memoize
    def uid(self):
        try:
            return self.context.UID()
        except AttributeError:
            return 'nouid'

    def css(self):
        return ""

    def js(self):
        return ""
