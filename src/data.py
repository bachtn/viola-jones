#!/usr/bin/env python3

import operator
import numpy as np
from sklearn.model_selection import train_test_split

class Data(object):
    """
    This class models a data used for training and testing a classfier.
    The data is characterized by:
    * list of attributes / features (length, width, ..)
    * list of classes / labels((dog / cat ...), (Binary classification: True / False), ... )
    * data (2d matrix containing the values of the features) Eg:  h = 3, w = 5
    * targets (1d array containing the labels (classes) of the data) Eg: 'dog'
    * train_percent = the percentage of the data used for training
        Eg: 0.8 -> 80% of data used for training and 20% used for testing
    """

    def __init__(self, features, labels, data, targets, train_percent):
        self.features = features
        self.labels = labels
        self.__data = data
        self.__targets = targets
        self.train_percent = train_percent
        (self.xtrain, self.xtest, self.ytrain, self.ytest) = Data.categorizeData(self.__data, self.__targets, self.train_percent)

    features = property(operator.attrgetter('_features'))

    @features.setter
    def features(self, features):
        if (not features or not isinstance(features, list)):
            raise ValueError("features should be a non empty list")
        self._features = features

    labels = property(operator.attrgetter('_labels'))

    @labels.setter
    def labels(self, value):
        if (not value or not isinstance(value, list) or len(value) < 2):
            raise ValueError("labels should be a list containing a minimum of 2 elements")
        self._labels = value

    __data = property(operator.attrgetter('_data'))

    @__data.setter
    def __data(self, data):
        # data.shape give (a, b) where a = nbr columns, b = nbr rows
        if (not isinstance(data, np.ndarray) or data.size == 0
            or (data.shape[1] != len(self.features))):
            raise ValueError("Data should be presented as a 2d non empty numpy array" +
                    " with n columns where n = nbr of features")
        self._data = data

    __targets = property(operator.attrgetter('_targets'))

    @__targets.setter
    def __targets(self, targets):
        if (not isinstance(targets, np.ndarray) or targets.size != self.__data.shape[0]
            or (targets.ndim != 1)):
            raise ValueError("Targets should be presented as a 1d non empty numpy array" +
                    " with 1 column and an equal size to the data matrix")
        self._targets = targets

    train_percent = property(operator.attrgetter('_train_percent'))

    @train_percent.setter
    def train_percent(self, train_percent):
        x = not train_percent or not isinstance(train_percent, float) or train_percent < 0.5 or train_percent > 0.9
        if (not train_percent or not isinstance(train_percent, float) or train_percent < 0.5 or train_percent > 0.9):
            raise ValueError("Train percentage should be a non empty float between 0.5 and 0.9")
        self._train_percent = train_percent

    def categorizeData(data, targets, train_percent):
        xtrain, xtest, ytrain, ytest = train_test_split(data, targets, train_size=train_percent)
        return (xtrain, xtest, ytrain, ytest)

    def __str__(self):
        return ("features = %s\nlabels = %s\ndata = %s\ntargets = %s\ntrain_percent = %s"
                % (self.features, self.labels, self.__data, self.__targets, self.train_percent))
