#!/usr/bin/env python3

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import numpy as np
from src.data import Data

class DataTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        features = ['height', 'width']
        labels = ['cat', 'dog']
        data = np.arange(10).reshape((5,2))
        targets = np.array([0,1,1,0,1])
        train_percent = 0.8
        self.data = Data(features, labels, data, targets, train_percent)

    @classmethod
    def tearDownClass(self):
        del self.data

    def testConstructor(self):
        # Empty arguments
        featuresArg = ['height', 'width']
        labelsArg = ['dog', 'cat']
        dataArg = np.zeros(shape=(4, 2))
        targetsArg = np.array([0,1,1,0])
        train_percent_arg = 0.8
        with self.assertRaises(TypeError): Data()
        with self.assertRaises(TypeError): Data(featuresArg)
        with self.assertRaises(TypeError): Data(featuresArg, labelsArg)
        with self.assertRaises(TypeError): Data(featuresArg, labelsArg, dataArg)
        with self.assertRaises(TypeError): Data(featuresArg, labelsArg, dataArg, targetsArg)

        # Should not fail
        try:
            Data(featuresArg, labelsArg, dataArg, targetsArg, train_percent_arg)
        except Exception as e:
            self.fail("Constructor raises exception: %s, while it should not" % type(e).__name__)
        trainPercents = [0.5, 0.9, 0.8]
        try:
            for valid_train_percent_arg in trainPercents:
                Data(features=featuresArg, labels=labelsArg, data=dataArg, targets=targetsArg, train_percent=valid_train_percent_arg)
        except Exception as e:
            self.fail("Constructor raises exception: %s, while it should not" % type(e).__name__)

        # Invalid arguments
        ## features
        with self.assertRaises(ValueError):
            Data(features=None, labels=labelsArg, data=dataArg, targets=targetsArg, train_percent=train_percent_arg)
        labelsInvalidArgs = [None, [1]]

        ## labels
        for invalidLabelsArg in labelsInvalidArgs:
            with self.assertRaises(ValueError):
                Data(features=featuresArg, labels=invalidLabelsArg, data=dataArg, targets=targetsArg, train_percent=train_percent_arg)

        ## data
        dataInvalidArgs = [None, [[0]*3]*4, np.zeros(shape=(4,1)), np.zeros(shape=(0,3))]
        for invalidDataArg in dataInvalidArgs:
            with self.assertRaises(ValueError):
                Data(features=featuresArg, labels=labelsArg, data=invalidDataArg, targets=targetsArg, train_percent=train_percent_arg)

        ## targets
        targetsInvalidArgs = [None, [[0]*3]*4, np.zeros(shape=(4,1)), np.zeros(shape=(4,2)), np.zeros(shape=(0,3))]
        for invalidTargetsArg in targetsInvalidArgs:
            with self.assertRaises(ValueError):
                Data(features=featuresArg, labels=labelsArg, data=dataArg, targets=invalidTargetsArg, train_percent=train_percent_arg)

        ## train_percent
        trainPercentInvalidArgs = [0., 0.4, 0.95, -0.2, -2., 5., 1., 100.]
        for invalid_train_percent_arg in trainPercentInvalidArgs:
            with self.assertRaises(ValueError):
                Data(features=featuresArg, labels=labelsArg, data=dataArg, targets=targetsArg, train_percent=invalid_train_percent_arg)

    def testCategorizeData(self):
        (xtrain, xtest, ytrain, ytest) = Data.categorizeData(self.data.getData(), self.data.getTargets(), self.data.train_percent)
        #TODO: add test
        pass

if __name__ == '__main__':
    unittest.main()
