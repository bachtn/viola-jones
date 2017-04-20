#!/usr/bin/env python3

import os
from PIL import Image
import numpy as np
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib

from utils import *
from integralImage import IntegralImage
from haar import Haar, HaarFeatureId
from data import Data

data = []
targets = []
haarFeatures = []
for haarId in HaarFeatureId:
    haarFeatures.append(Haar(haarId, False))

def setUpClassifier(dataValues, targetValues):
    dataValues = np.asarray(dataValues)
    targetValues = np.asarray(targetValues)
    features = [HaarFeatureId.A2VWB.name, HaarFeatureId.C3WBW.name,
            HaarFeatureId.C3WBW.name, HaarFeatureId.D4WBBW.name, 'size']
    labels = [1,0]
    dataObject = Data(features, labels, dataValues, targetValues, 0.8)
    clf = AdaBoostClassifier()
    # train classifier
    clf.fit(dataObject.xtrain, dataObject.ytrain)

    # test classifier
    predicted = clf.predict(dataObject.xtest)
    expected = dataObject.ytest
    accuracy = accuracy_score(expected, predicted)
    print("accuracy = %.2f" % accuracy)

    # Export classifier for future use
    joblib.dump(clf, 'trained-classifier.pkl')
    #clfNew = joblib.load('trained-classifier')

def createData(dataDirPath = os.getcwd() + "/samples/data"):
    """
    dataDirPath = the path to the directory containing data
    """
    positiveDataPath = dataDirPath + "/positive"
    negativeDataPath = dataDirPath + "/negative"
    iterateOverData(positiveDataPath, 1)
    iterateOverData(negativeDataPath, 0)
    #print("final data size = %d" % (len(targets)))
    setUpClassifier(data, targets)

def iterateOverData(dataPath, dataType):
    """
    dataPath = the path to the positive or negative data
    dataType = positiveData ? 1 : 0
    """
    string = ",".join(map(str, haarFeatures))
    for subdir, dirs, files in os.walk(dataPath):
        for fileName in files:
            if (fileName.endswith(('.jpg', '.jpeg', '.png'))):
                dataFilePath = os.path.join(subdir, fileName)
                createDataFromPath(dataFilePath, dataType)


def createDataFromPath(imgPath, dataType):
    """
    filePath represents the path of the data file
    targetId = {1, 0}: 1 -> yes, 0 -> no
    """
    tmp = normalizeImageData(imgPath)
    normalizedData = tmp['data']
    size = tmp['size']
    integralImage = getIntegralImage(normalizedData, size)
    createDataFromImage(integralImage, 1, 24, dataType)


def createDataFromImage(integralImage, windowStep, minWindowSize, dataType):
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
        computeHaarForGivenSize(integralImage, windowSize, allCoordinates, dataType)

def computeHaarForGivenSize(integralImage, windowSize, allCoordinates, dataType):
    for (x,y) in allCoordinates:
        dataTmp = []
        for haar in haarFeatures:
            value = haar.computeHaar(x, y, windowSize, integralImage)
            dataTmp.append(value)
            #TODO targetId can be generated from the size of data
        dataTmp.append(windowSize)
        data.append(dataTmp)
        targets.append(dataType)

