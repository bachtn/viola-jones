#!/usr/bin/env python3

import os
from PIL import Image
import numpy as np
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

from utils import *
from integralImage import IntegralImage
from haar import Haar, HaarFeatureId
from data import Data
from classify import *


def predict(imgPath, clfName):
    clf = joblib.load(clfName)
    tmp = normalizeImageData(imgPath)
    normalizedData = tmp['data']
    size = tmp['size']
    integralImage = getIntegralImage(normalizedData, size)
    allCoord = []
    preparedData = prepareData(integralImage, 5, 20, allCoord)
    dataValues = np.asarray(preparedData)
    predicted = clf.predict(dataValues)
    drawRectangles(allCoord, predicted, preparedData)
    """
    predicted_str = '\n'.join(map(str, predicted.tolist()))
    dataValues_str = '\n'.join(map(str, dataValues))
    allCoord = '\n'.join(map(str, allCoord))
    fp = open('predictionResult', 'w')
    fd = open('dataResult', 'w')
    fc = open('coordinates', 'w')
    fp.write(predicted_str)
    fd.write(dataValues_str)
    fc.write(allCoord)
    fp.close()
    fd.close()
    fc.close()
    """


def drawRectangles(allCoord, predicted, preparedData):
    positiveIndexes = np.where(predicted == 1)
    im = np.array(Image.open('test.jpg'), dtype=np.uint8)
    fig, ax = plt.subplots(1)
    ax.imshow(im)
    for index in positiveIndexes[0]:
        x, y = allCoord[index]
        size = preparedData[index][4:][0]
        rect = ptc.Rectangle((x, y), size, size, linewidth=1,
                edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    plt.show()


def prepareData(integralImage, windowStep, minWindowSize, allCoord):
    preparedData = []
    width, height = integralImage.size
    xs, ys = [], []
    # All possible window sizes
    maxSquare = width if width <= height else height
    possibleSizes = np.arange(minWindowSize, maxSquare, windowStep)
    if (maxSquare % windowStep != 0):
        possibleSizes = np.append(possibleSizes, maxSquare)
    fp = open('coordinates', 'w')
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
        allCoord.extend(allCoordinates)
        allCoordinates_str = '\n'.join(map(str, allCoordinates))
        #fp.write("window size = %d" % windowSize)
        #fp.write(allCoordinates_str)
        preparedData.extend(prepareSubWindow(integralImage, windowSize, allCoordinates))
    fp.close()
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


