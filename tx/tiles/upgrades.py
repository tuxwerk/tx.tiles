from Products.CMFCore.utils import getToolByName
from tx.tiles.importexport import install

default_profile = 'profile-tx.tiles:default'


def upgrade_rolemap(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')


def upgrade_controlpanel(context):
    context.runImportStepFromProfile(default_profile, 'controlpanel')


def upgrade_collection(context):
    install(context)
