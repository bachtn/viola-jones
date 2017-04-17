#!/usr/bin/env python3

import os
from PIL import Image
import numpy as np
from src.integralImage import IntegralImage
from src.haar import Haar, HaarFeatureId
from src.data import Data

data = []
targets = []
haarFeatures = []
for haarId in HaarFeatureId:
    haarFeatures.extend([Haar(haarId, True), Haar(haarId, False)])

def createData(dataDirPath = os.getcwd() + "/samples/data"):
    """
    dataDirPath = the path to the directory containing data
    """
    positiveDataPath = dataDirPath + "/positive"
    negativeDataPath = dataDirPath + "/negative"
    iterateOverData(positiveDataPath, 1)
    iterateOverData(negativeDataPath, 0)

def iterateOverData(dataPath, dataType):
    """
    dataPath = the path to the positive or negative data
    dataType = positiveData ? 1 : 0
    """
    string = ",".join(map(str, haarFeatures))
    print(string)
    for subdir, dirs, files in os.walk(dataPath):
        for fileName in files:
            if (fileName.endswith(('.jpg', '.jpeg', '.png'))):
                dataFilePath = os.path.join(subdir, fileName)
                createDataFromPath(dataFilePath, dataType)


def createDataFromPath(filePath, dataType):
    """
    filePath represents the path of the data file
    targetId = {1, 0}: 1 -> yes, 0 -> no
    """
    image = openImage(filePath)
    image = toGrayscale(image)
    integralImage = getIntegralImage(image)
    createDataFromImage(integralImage, 5, 20)


def createDataFromImage(integralImage, windowStep, minWindowSize):
    width, height = integralImage.size
    xs, ys = [], []
    print("height = %d, width = %d, windowStep = %d" % (height, width, windowStep))
    # All possible window sizes
    maxSquare = width if width <= height else height
    possibleSizes = np.arange(minWindowSize, maxSquare, windowStep)
    if (maxSquare % windowStep != 0):
        possibleSizes = np.append(possibleSizes, maxSquare)
    print("possibleSizes = %s" % possibleSizes)
    for windowSize in possibleSizes:
        # All possible x coordinates
        xs = np.arange(0, width - windowStep, windowSize) if windowSize != width else [0]
        if (width % windowSize != 0): xs = np.append(xs, width - windowSize)
        # All possible y coordinates
        ys = np.arange(0, height - windowSize, windowSize) if windowSize != height else [0]
        if (height % windowSize != 0): ys = np.append(ys, height - windowSize)
        print("size = %d, xs = %s, ys = %s" % (windowSize, xs, ys))
        for x in xs:
            for y in ys:
                continue


def openImage(imagePath):
    im = Image.open(imagePath)
    return im

def dataToList(image):
    data = []
    for i in list(image.getdata()): #getdata contains an RGB(tuple) array
        for j in i:
            data.append(j)
    return data

def toImage(imageData, size, mode):
    newImage = Image.new(mode, size)
    newImage.putdata(imageData)
    return newImage

def toGrayscale(image):
    return image.convert('LA')

def getIntegralImage(image):
    return IntegralImage(image.size, dataToList(image))

def saveToFile(data, filename):
    dataFile = open(filename, 'w')
    for item in data:
        dataFile.write("%s " % item)
