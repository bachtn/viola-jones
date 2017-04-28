#!/usr/bin/env python3

import os
from PIL import Image
import numpy as np
import csv
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

def exportDataToCSV(dataToExport, filename):
    with open(filename, 'wb') as csvFile:
        wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
        wr.writerow(dataToExport)

def setUpClassifier(dataValues, targetValues):
    dataValues = np.asarray(dataValues)
    targetValues = np.asarray(targetValues)
    features = [HaarFeatureId.A2VWB.name, HaarFeatureId.C3WBW.name,
            HaarFeatureId.C3WBW.name, HaarFeatureId.D4WBBW.name]
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


def createData(dataDirPath = os.getcwd() + "/samples"):
    """
    dataDirPath = the path to the directory containing data
    """
    createPositiveData()
    createNegativeData()
    setUpClassifier(data, targets)

def createPositiveData():
    print("Training with positive dataset")
    with open('samples/pos/info.lst') as f:
        content = f.readlines()

    for ln in content:
        lnC = ln.rstrip().split(' ')
        filename = 'samples/pos/' + lnC[0]
        createDataFromPath(datatype=1, imgPath=filename)


def createNegativeData():
    print("Training with negative dataset")
    with open('samples/neg/bg.txt') as f:
        content = f.readlines()

    for ln in content:
        lnC = ln.rstrip().split(' ')
        filename = 'samples/' + lnC[0]
        createDataFromPath(datatype=0, imgPath=filename)

def createDataFromPath(**kwargs):
    datatype = kwargs['datatype']
    imgPath = kwargs['imgPath']
    tmp = normalizeImageData(imgPath)
    normalizedData = tmp['data']
    size = tmp['size']
    integralImage = getIntegralImage(normalizedData, size)
    createDataFromImage(integralImage, datatype)


def createDataFromImage(integralImage, dataType):
    computeHaarForGivenSize(integralImage, dataType)

def computeHaarForGivenSize(integralImage, datatype):
    dataTmp = []
    x, y = 0, 0
    width, height = integralImage.size
    size = width if (width <= height) else height
    #print("width = %d, height = %d, size = %d" % (width, height, size))
    for haar in haarFeatures:
        # width = height = size in the training case
        value = haar.computeHaar(x, y, size, integralImage)
        dataTmp.append(value)
    data.append(dataTmp)
    targets.append(datatype)

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
