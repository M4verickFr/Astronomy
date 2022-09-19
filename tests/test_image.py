# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from Astronomy.image import *


class TestImportImage(unittest.TestCase):

    def test_coordinateToUrl():
        ra = "13 39."
        decl =  "-31 4"
        urlFromCoordinate = coordinateToUrl(ra, decl)
        url = "https://archive.stsci.edu/cgi-bin/dss_search\?v\=3\&r\=13+39+53.2\&d\=-31+40+15.0\&h\=10.0\&w\=10.0\&f\=fits"
        self.assertEqual(urlFromCoordinate, url)

if __name__ == '__main__':
    unittest.main()
