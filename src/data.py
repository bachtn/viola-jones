#!/usr/bin/env python3

import operator
import numpy as np

class Data(object):
    """
    This class models a data used for training and testing a classfier.
    The data is characterized by:
    * list of attributes / features (length, width, ..)
    * list of classes / labels((dog / cat ...), (Binary classification: True / False), ... )
    * data (values and their corresponding class (features + labels)
      Eg:  h = 3, w = 5, class = dog)
    * training_data -> data for training
    * testing_data -> data for testing
    """

    def __init__(self, features, labels, data):
        self.features = features
        self.labels = labels
        self.__data = data
        #(self.training_data, self.testing_data) = Data.categorizeData(self.data)

    features = property(operator.attrgetter('_features'))

    @features.setter
    def features(self, features):
        if (not features or not isinstance(features, list)):
            raise ValueError("features should be a non empty list")
        self._features = features

    labels = property(operator.attrgetter('_labels'))

    @labels.setter
    def labels(self, labels):
        if (not labels or not isinstance(labels, list) or len(labels) < 2):
            raise ValueError("labels should be a list containing a minimum of 2 elements")
        self._labels = labels

    __data = property(operator.attrgetter('_data'))

    @__data.setter
    def __data(self, data):
        # data.shape give (a, b) where a = nbr columns, b = nbr rows
        if (not isinstance(data, np.ndarray) or data.size == 0
            or (data.shape[1] != len(self.features) + 1)):
            raise ValueError("Data should be presented as a 2d non empty numpy array" +
                    " with n columns where n = nbr of features + 1")
        self._data = data

    def categorizeData(data):
        pass
