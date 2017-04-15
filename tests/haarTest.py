#!/usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from src.haar import Haar
from src.haar import HaarFeatureId
from src.integralImage import IntegralImage

class HaarTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def testConstructor(self):
        pass

    def testComputeHaar(self):
        pass

    def testComputeHaarA2VWB(self):
        pass

    def testComputeHaarB2HWB(self):
        pass

    def testComputeHaarC3WBW(self):
        pass

    def testComputeHaarD4WBBW(self):
        pass

if __name__ == '__main__':
    unittest.main()
