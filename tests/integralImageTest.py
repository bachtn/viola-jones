#! /usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from src.integralImage import IntegralImage


class IntegralImageTestCases(unittest.TestCase):

    ### The following are special methods

    @classmethod
    def setUpClass(self):
        data = [3,8,2,1,
                6,3,9,7,
                5,2,4,9,
                6,0,1,8]
        size = (4,4)
        self.integralImage = IntegralImage(size, data)

    @classmethod
    def tearDownClass(self):
        del self.integralImage


    ### Here comes the user test methods
    def testIntegralImageCalculation(self):
        expectedIntegral = [
                3,11,13,14,
                9,20,31,39,
                14,27,42,59,
                20,33,49,74]
        self.assertListEqual(self.integralImage.integral, expectedIntegral)

    def testGet(self):
        #TODO
        pass

    def testGetSubWindow(self):
        self.assertEqual(self.integralImage.getSubWindow(0, 0, 4), 74)
        self.assertEqual(self.integralImage.getSubWindow(2, 2, 2), 22)
        self.assertEqual(self.integralImage.getSubWindow(2, 2, 1), 4)


    def testGenrate(self):
        #TODO
        pass

if __name__ == '__main__':
    unittest.main()
