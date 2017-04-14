
class IntegralImage(object):
    """
    data = pixel values of original image
    size, width, height = size, width, height of the image
    """
    def __init__(self, size, data):
        self.size = size
        self.data = data
        width, height = self.size
        self.integral = [None for _ in range(width * height)]
        self.generate()

    def generate(self):
        width, height = self.size
        self.integral = [self.get(x, y) for y in range(height) for x in range(width)]
        """integralTmp = []
        sumValue = 0
        for j in range(0, self.height - 1):
            for i in range(0, self.width - 1):
                sumValue = sumValue + self.data[self.getIndex(i, j)]
                integralTmp.append(sumValue)
        return integralTmp
        """

    def getIndex(self, x, y):
        return y * self.width + x

    def get(self, x, y):
        width, height = self.size
        index = y * width + x
        if(x < 0 or y < 0):
             # value at negative-indexed point is always 0
             return 0
        elif self.integral[index] is not None:
             # if the value at point x, y has already been generated
             return self.integral[index]
        else:
            cummulative = self.get(x - 1, y) + self.get(x, y - 1) - self.get(x - 1, y - 1) + self.data[index]
            self.integral[index] = cummulative
            return cummulative
