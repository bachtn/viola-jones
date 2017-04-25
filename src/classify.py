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
    createNegativeData()
    createPositiveData()
    setUpClassifier(data, targets)

def createPositiveData():
    print("Training with positive dataset")
    with open('samples/pos/info.lst') as f:
        content = f.readlines()

    i = 0
    for ln in content:
        lnC = ln.rstrip().split(' ')
        filename = 'samples/pos/' + lnC[0]
        x = int(lnC[1])
        y = int(lnC[2])
        w = int(lnC[3])
        h = int(lnC[4])
        createDataFromPath(datatype=1, imgPath=filename, \
                xCoord=x, yCoord=y, width=w, height=h)
        i += 1
        print(i)


def createNegativeData():
    print("Training with negative dataset")
    with open('samples/neg/bg.txt') as f:
        content = f.readlines()

    i = 0

    for ln in content:
        lnC = ln.rstrip().split(' ')
        filename = 'samples/' + lnC[0]
        createDataFromPath(datatype=0, imgPath=filename)
        i += 1
        print(i)

def createDataFromPath(**kwargs):
    """
    filePath represents the path of the data file
    targetId = {1, 0}: 1 -> yes, 0 -> no
    """
    datatype = kwargs['datatype']
    imgPath = kwargs['imgPath']
    tmp = normalizeImageData(imgPath)
    normalizedData = tmp['data']
    size = tmp['size']
    integralImage = getIntegralImage(normalizedData, size)
    if (datatype == 0):
        createDataFromImage(integralImage, 5, 24, datatype)
    else:
        x = kwargs['xCoord']
        y = kwargs['yCoord']
        w = kwargs['width']
        h = kwargs['height']
        createDataFromImage(integralImage, 5, 24, datatype, \
                xCoord=x, yCoord=y, width=w, height=h)


def createDataFromImage(integralImage, step, minSize, dataType, **kwargs):
    width, height = integralImage.size
    xs, ys = [], []
    # All possible window sizes
    maxSquare = width if width <= height else height
    possibleSizes = np.arange(minSize, maxSquare, step)
    if (maxSquare % step != 0):
        possibleSizes = np.append(possibleSizes, maxSquare)

    for windowSize in possibleSizes:
        # All possible x coordinates
        xs = np.arange(0, width - windowSize, windowSize) \
                if windowSize != width else [0]
        if (width % windowSize != 0): xs = np.append(xs, width - windowSize)

        # All possible y coordinates
        ys = np.arange(0, height - windowSize, windowSize) \
                if windowSize != height else [0]
        if (height % windowSize != 0): \
                ys = np.append(ys, height - windowSize)

        # Generate all combinations between possible x and y coordinates
        allCoordinates = [[x,y] for x in xs for y in ys]
        computeHaarForGivenSize(integralImage, windowSize, \
                allCoordinates, dataType, **kwargs)

def computeHaarForGivenSize(integralImage, windowSize, \
        allCoordinates, datatype, **kwargs):
    for (x,y) in allCoordinates:
        dataTmp = []

        for haar in haarFeatures:
            value = haar.computeHaar(x, y, windowSize, integralImage)
            dataTmp.append(value)
            #TODO targetId can be generated from the size of data
        dataTmp.append(windowSize)
        data.append(dataTmp)

        subWData = datatype

        if (datatype == 1):
            x0 = kwargs['xCoord']
            y0 = kwargs['yCoord']
            w0 = kwargs['width']
            h0 = kwargs['height']
            subWData = getDataType(x0, y0, w0, h0, x, y, windowSize, windowSize)
        targets.append(subWData)

def getDataType(x0, y0, w0, h0, x, y, w, h):
    """
    x, y ... => subWindow
    x0, y0 ... => object
    """
    isObject = x >= x0 and x < x0 + w0 and y >= y0 and y < y0 + h0
    return 1 if isObject else 0


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
                createDataFromPath(dataFilePath, **kwargs)
