#!/usr/bin/env python3

import os
from PIL import Image
from integralImage import IntegralImage
from haar import Haar, HaarFeatureId
from data import Data

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
    image.show()


def createDataFromImage(imagePath):
    pass




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
    return integralImage(image)

def saveToFile(data, filename):
    dataFile = open(filename, 'w')
    for item in data:
        dataFile.write("%s " % item)
