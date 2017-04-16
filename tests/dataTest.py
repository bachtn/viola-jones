#!/usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import numpy as np
from src.data import Data

class DataTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def testConstructor(self):
        # Empty arguments
        featuresArg = ['height', 'width']
        labelsArg = ['dog', 'cat']
        dataArg = np.zeros(shape=(4, 3))
        with self.assertRaises(TypeError): Data()
        with self.assertRaises(TypeError): Data(featuresArg)
        with self.assertRaises(TypeError): Data(featuresArg, labelsArg)
        # Should not fail
        try:
            Data(featuresArg, labelsArg, dataArg)
        except Exception as e:
            self.fail("Constructor raises exception: %s, while it should not" % type(e).__name__)
        # Invalid arguments
        with self.assertRaises(ValueError):
            Data(features=None, labels=labelsArg, data=dataArg)
        labelsInvalidArgs = [None, [1]]
        for labelsArg in labelsInvalidArgs:
            with self.assertRaises(ValueError):
                Data(features=featuresArg, labels=labelsArg, data=dataArg)
        dataInvalidArgs = [None, [[0]*3]*4, np.zeros(shape=(4,1)),
                np.zeros(shape=(4,2)), np.zeros(shape=(0,3))]
        for dataArg in dataInvalidArgs:
            with self.assertRaises(ValueError):
                Data(features=featuresArg, labels=labelsArg, data=dataArg)



if __name__ == '__main__':
    unittest.main()
