from tx.tiles.interfaces import ITilesPage
from zope.interface import noLongerProvides
from zope.annotation.interfaces import IAnnotations
from tx.tiles import logger

def remove_annotations(items_to_check):
    for item in items_to_check:
        item = item.getObject()
        logger.info("Removing tiles data for %s" % (
            '/'.join(item.getPhysicalPath())))
        noLongerProvides(item, ITilesPage)
        item.reindexObject(idxs=['object_provides'])

        annotations = IAnnotations(item)
        metadata = annotations.get('tx.tiles', None)
        if metadata is not None:
            del annotations['tx.tiles']

def install(context):
    return

def uninstall(context):

    if context.readDataFile('tx.tiles-uninstall.txt') is None:
        return

    portal = context.getSite()
    catalog = portal.portal_catalog
    
    remove_annotations(catalog.searchResults(
        object_provides=ITilesPage.__identifier__))
