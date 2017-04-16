#!/usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from src.haar import HaarFeatureId
from src.haar import Haar
from src.integralImage import IntegralImage

class HaarTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.haar = Haar(HaarFeatureId(1), False)
        data = [1,2,3,4,
                5,6,7,8,
                9,10,11,12,
                13,14,15,16]
        size = (4,4)
        self.integralImage = IntegralImage(size, data)

    @classmethod
    def tearDownClass(self):
        del self.integralImage
        del self.haar

    def testConstructor(self):
        # Wrong argument's type
        with self.assertRaises(ValueError): Haar(1, False)
        with self.assertRaises(ValueError): Haar(HaarFeatureId(1), 'wrong argument')
        # missing arguments
        with self.assertRaises(TypeError): Haar(HaarFeatureId(1))
        with self.assertRaises(TypeError): Haar(False)
        with self.assertRaises(TypeError): Haar()
        # Should not fail
        try:
            Haar(HaarFeatureId(1), False)
        except Exception as e:
            self.fail("Constructor raises exception: %s, while it should not" % type(e).__name__)

    def testComputeHaar(self):
        value = self.haar.computeHaar(2, 2, 2, self.integralImage)
        self.assertEqual(value, -2)

    def testComputeHaarA2VWB(self):
        value = Haar.computeHaarA2VWB(HaarFeatureId(1), 2, 2, 2, self.integralImage)
        self.assertEqual(value, -2)

    def testComputeHaarB2HWB(self):
        value = Haar.computeHaarB2HWB(HaarFeatureId(2), 2, 2, 2, self.integralImage)
        self.assertEqual(value, -8)

    def testComputeHaarC3WBW(self):
        value = Haar.computeHaarC3WBW(HaarFeatureId(3), 1, 1, 3, self.integralImage)
        self.assertEqual(value, 33)

    def testComputeHaarD4WBBW(self):
        value = Haar.computeHaarD4WBBW(HaarFeatureId(4), 2, 2, 2, self.integralImage)
        self.assertEqual(value, 0)
        value = Haar.computeHaarD4WBBW(HaarFeatureId(4), 1, 1, 3, self.integralImage)
        self.assertEqual(value, 21)

if __name__ == '__main__':
    unittest.main()
