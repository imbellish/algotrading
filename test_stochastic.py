__author__ = 'imbellish'

import unittest
import yahoo_finance
from testdata import testdata

from stochastic import *

class TestStochastic(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_stats(self):
        start = '2015-08-17'
        end = '2015-08-17'

    def test_get_k(self):
        observed = K(testdata)
        expected = 152.31889237552127
        self.assertEqual(observed, expected)

    def test_get_d(self):
        pass

if __name__ == '__main__':
    #for row in testdata:
    #    print(row)
    unittest.main()
