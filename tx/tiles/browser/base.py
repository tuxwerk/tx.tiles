from plone.memoize.view import memoize

class AbstractTilesView(object):
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
