from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='tx.tiles',
      version=version,
      description="Image tiles for article teasers.",
      long_description='%s\n%s' % (
          open("README.rst").read(),
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Plone :: 4.3"
      ],
      keywords='plone tiles',
      author='Marek Kralewski',
      author_email='info@tuxwerk.de',
      url='https://github.com/tuxwerk/tx.tiles/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tx'],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
          'collective.js.jqueryui'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """)