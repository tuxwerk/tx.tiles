from tx.slider.interfaces import ISliderPage
from zope.interface import noLongerProvides
from zope.annotation.interfaces import IAnnotations
from tx.slider import logger

def remove_annotations(items_to_check):
    for item in items_to_check:
        item = item.getObject()
        logger.info("Removing slider data for %s" % (
            '/'.join(item.getPhysicalPath())))
        noLongerProvides(item, ISliderPage)
        item.reindexObject(idxs=['object_provides'])

        annotations = IAnnotations(item)
        metadata = annotations.get('tx.slider', None)
        if metadata is not None:
            del annotations['tx.slider']

def install(context):
    return

def uninstall(context):

    if context.readDataFile('tx.slider-uninstall.txt') is None:
        return

    portal = context.getSite()
    catalog = portal.portal_catalog
    
    remove_annotations(catalog.searchResults(
        object_provides=ISliderPage.__identifier__))
