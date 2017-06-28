from Products.CMFCore.utils import getToolByName
from tx.slider.importexport import install

default_profile = 'profile-tx.slider:default'


def upgrade_rolemap(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')


def upgrade_controlpanel(context):
    context.runImportStepFromProfile(default_profile, 'controlpanel')


def upgrade_collection(context):
    install(context)
