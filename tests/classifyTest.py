#! /usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
from src.integralImage import IntegralImage
from src.classify import *


class ClassifyTestCases(unittest.TestCase):

    ### The following are special methods

    @classmethod
    def setUpClass(self):
        data = list(range(56))
        size = (8,7)
        self.integralImage = IntegralImage(size, data)

    @classmethod
    def tearDownClass(self):
        del self.integralImage


    def testCreateDataFromImage(self):
        infos = createDataFromImage(self.integralImage, 3, 3)

if __name__ == '__main__':
    unittest.main()
