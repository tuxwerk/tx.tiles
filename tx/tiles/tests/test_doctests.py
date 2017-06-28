import unittest2 as unittest
from Testing import ZopeTestCase as ztc
from tx.tiles.tests import BaseFunctionalTest


def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'browser.txt', package='tx.tiles',
            test_class=BaseFunctionalTest)])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
