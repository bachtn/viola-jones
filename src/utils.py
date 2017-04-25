#!/usr/bin/env python3

from PIL import Image
import numpy as np

from integralImage import IntegralImage

def openImage(imgPath):
    return Image.open(imgPath)

def getImgData(img):
    """
    Return the img data as a list of tuple containing RGB/Grayscale values
    """
    pixelValues = []
    for pixel in list(img.getdata()):
        for value in pixel:
            pixelValues.append(value)
    return pixelValues

def createImage(pixelValues, size, mode):
    """
    given img data, size and PIL mode(rgd, grayscale ...), create img
    """
    newImg = Image.new(mode, size)
    newImg.putdata(pixelValues)
    return newImg

def convertToGrayscale(img):
    return img.convert('LA')

def saveDataToFile(data, filename):
    dataFile = open(filename, 'w')
    for item in data: dataFile.write("%s " % item)
    dataFile.close()

def getIntegralImage(imgData, size):
    return IntegralImage(size, imgData)

@np.vectorize
def normalize(x, mean, std):
    return (x - mean) / std

def calculateMean(imgData):
    return np.mean(imgData)

def calculateStd(imgData):
    return np.var(imgData)

def normalizeImageData(imgPath):
    img = openImage(imgPath)
    img = convertToGrayscale(img)
    data = np.asarray(getImgData(img))
    mean = calculateMean(data)
    std = calculateStd(data)
    normalizedData = normalize(data, mean, std)
    return {'data': normalizedData, 'size': img.size}
