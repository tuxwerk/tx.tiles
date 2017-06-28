import unittest2 as unittest
from Testing import ZopeTestCase as ztc
from tx.slider.tests import BaseFunctionalTest


def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'browser.txt', package='tx.slider',
            test_class=BaseFunctionalTest)])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
