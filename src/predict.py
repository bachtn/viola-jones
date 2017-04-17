#!/usr/bin/env python3

import os
from PIL import Image
import numpy as np
from integralImage import IntegralImage
from haar import Haar, HaarFeatureId
from data import Data
from classify import *
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib


def predict(imagePath, clfName):
    clf = joblib.load(clfName)
    image = openImage(imagePath)
    image.show()
    """
    image = toGrayscale(image)
    integralImage = getIntegralImage(image)
    preparedData = prepareData(integralImage, 5, 20)
    dataValues = np.asarray(preparedData)
    predicted = clf.predict(dataValues)
    print(predicted)
    predicted_str = '\n'.join(map(str, predicted.tolist()))
    dataValues_str = '\n'.join(map(str, dataValues))
    """
    """
    fp = open('predictionResult', 'w')
    fd = open('dataResult', 'w')
    fp.write(predicted_str)
    fd.write(dataValues_str)
    fp.close()
    fd.close()
    """


def prepareData(integralImage, windowStep, minWindowSize):
    preparedData = []
    width, height = integralImage.size
    xs, ys = [], []
    # All possible window sizes
    maxSquare = width if width <= height else height
    possibleSizes = np.arange(minWindowSize, maxSquare, windowStep)
    if (maxSquare % windowStep != 0):
        possibleSizes = np.append(possibleSizes, maxSquare)
    for windowSize in possibleSizes:

        # All possible x coordinates
        xs = np.arange(0, width - windowSize, windowSize) if windowSize != width else [0]
        if (width % windowSize != 0): xs = np.append(xs, width - windowSize)

        # All possible y coordinates
        ys = np.arange(0, height - windowSize, windowSize) if windowSize != height else [0]
        if (height % windowSize != 0): ys = np.append(ys, height - windowSize)
        #print("data size = %d" % (len(targets)))
        #print("sizes = %s\n\n\nxs = %s\n\n\nys = %s\n\n\n" % (possibleSizes, xs, ys))
        # Generate all combinations between possible x and y coordinates
        allCoordinates = [[x,y] for x in xs for y in ys]
        preparedData.extend(prepareSubWindow(integralImage, windowSize, allCoordinates))
    return preparedData

def prepareSubWindow(integralImage, windowSize, allCoordinates):
    preparedData = []
    for (x,y) in allCoordinates:
        dataTmp = []
        for haar in haarFeatures:
            value = haar.computeHaar(x, y, windowSize, integralImage)
            dataTmp.append(value)
            #TODO targetId can be generated from the size of data
        dataTmp.append(windowSize)
        preparedData.append(dataTmp)
    return preparedData


