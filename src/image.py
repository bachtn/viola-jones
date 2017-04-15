#!/usr/bin/env python3

from PIL import Image
from typing import List
from integralImage import *

def main():
    image = openImage("samples/lena.png")
    image = toGrayscale(image)
    image.show()

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

if __name__ == '__main__':
    main()
