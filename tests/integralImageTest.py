#! /usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from src.integralImage import IntegralImage


class IntegralImageTestCases(unittest.TestCase):

    ### The following are special methods

    @classmethod
    def setUpClass(self):
        data1 = [3,8,2,1,
                6,3,9,7,
                5,2,4,9,
                6,0,1,8]
        data2 = [1,2,3,4,
                5,6,7,8,
                9,10,11,12,
                13,14,15,16]
        size = (4,4)
        self.integralImage1 = IntegralImage(size, data1)
        self.integralImage2 = IntegralImage(size, data2)

    @classmethod
    def tearDownClass(self):
        del self.integralImage1
        del self.integralImage2


    ### Here comes the user test methods
    def testIntegralImageCalculation(self):
        expectedIntegral1 = [
                3,11,13,14,
                9,20,31,39,
                14,27,42,59,
                20,33,49,74]
        expectedIntegral2 = [
                1,3,6,10,
                6,14,24,36,
                15,33,54,78,
                28,60,96,136]
        self.assertListEqual(self.integralImage1.integral, expectedIntegral1)
        self.assertListEqual(self.integralImage2.integral, expectedIntegral2)

    def testGet(self):
        #TODO
        pass

    def testGetSubWindow(self):
        # integralImage1
        self.assertEqual(self.integralImage1.getSubWindow(0, 0, 4, 4), 74)
        self.assertEqual(self.integralImage1.getSubWindow(2, 2, 2, 2), 22)
        self.assertEqual(self.integralImage1.getSubWindow(2, 2, 1, 1), 4)
        # integralImage2
        """
        Haar Feature A
        -----
        |0|1|
        |0|1|
        -----
        """
        self.assertEqual(self.integralImage2.getSubWindow(2, 2, 1, 2), 26)
        self.assertEqual(self.integralImage2.getSubWindow(3, 2, 1, 2), 28)


    def testGenrate(self):
        #TODO
        pass

if __name__ == '__main__':
    unittest.main()
