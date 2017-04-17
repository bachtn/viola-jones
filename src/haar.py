#!/usr/bin/env python3

from enum import Enum
import operator
import typing

class HaarFeatureId(Enum):
    A2VWB = 1   # -> 01     -- 2 Vertical blocks White Black
    B2HWB = 2   # -> 0/1    -- 2 Horizontal blocks White Black
    C3WBW = 3   # -> 010    -- 3 vertical blocks White Black White
    D4WBBW = 4  # -> 01/10  -- 4 horizontal / vertical blocks
                # White Black Black White

class Haar(object):
    """
    This class models a Haar Feature.
    A Haar Feature is represented by its id: haar_id and the order
    of the blocks eg: White Black or Black White ....
    This is managed by the attribute is_inverted.
    Given a haar_id, an integralImage and the information of a subwindow
    (coordinates, size), we can compute the differance between
    the subwindow and the haar feature.
    """
    def __init__(self, haar_id, is_inverted):
        self.haar_id = haar_id
        self.is_inverted = is_inverted

    # The proper way to test constructor arguments
    haar_id = property(operator.attrgetter('_haar_id'))

    @haar_id.setter
    def haar_id(self, haar_id):
        if not haar_id or not isinstance(haar_id, HaarFeatureId):
            raise ValueError("haar_id should be one of the HaarFeatureId class values")
        self._haar_id = haar_id

    is_inverted = property(operator.attrgetter('_is_inverted'))

    @is_inverted.setter
    def is_inverted(self, is_inverted):
        if not isinstance(is_inverted, bool):
            raise ValueError("is_inverted should be True or False")
        self._is_inverted = is_inverted

    def computeHaar(self, x, y, size, integralImage):
        #TODO implment visitor design pattern so that you will not
        # need to check what method you want to call
        #TODO: correct dictionary
        """
        **locals() gives all the local variables: x, y ...
        => you should not declare variables before using it if you need only to pass function arguments
        """
        """
        return {
                HaarFeatureId.A2VWB: Haar.computeHaarA2VWB(self.haar_id, x, y, size, integralImage),
                HaarFeatureId.B2HWB: Haar.computeHaarB2HWB(self.haar_id, x, y, size, integralImage),
                HaarFeatureId.C3WBW: Haar.computeHaarC3WBW(self.haar_id, x, y, size, integralImage),
                HaarFeatureId.D4WBBW: Haar.computeHaarD4WBBW(self.haar_id, x, y, size, integralImage)
                }[self.haar_id]
        """
        value = 0
        if (self.haar_id == HaarFeatureId.A2VWB):
            value = Haar.computeHaarA2VWB(self.haar_id, x, y, size, integralImage)
        elif (self.haar_id == HaarFeatureId.B2HWB):
            value = Haar.computeHaarB2HWB(self.haar_id, x, y, size, integralImage)
        elif (self.haar_id == HaarFeatureId.C3WBW):
            value = Haar.computeHaarC3WBW(self.haar_id, x, y, size, integralImage)
        elif (self.haar_id == HaarFeatureId.D4WBBW):
            value = Haar.computeHaarD4WBBW(self.haar_id, x, y, size, integralImage)
        else: raise ValueError("Invalid haarId")
        return -1 * value if self.is_inverted else value

    def computeHaarA2VWB(haar_id, x, y, size, integralImage):
        """
        -------  --------  --------
        |00|11|  |00|111|  |000|11|
        |00|11|  |00|111|  |000|11|
        -------  --------  --------
        """
        if (haar_id != HaarFeatureId.A2VWB):
            raise ValueError("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.A2VWB.name, haar_id.name))
        else:
            (a, b) = (size // 2, size % 2)
            firstValue = integralImage.getSubWindow(x, y, a, size)
            secondValue = integralImage.getSubWindow(x + a, y, a + b, size)
            resultSubstraction = firstValue - secondValue
            return resultSubstraction



    def computeHaarB2HWB(haar_id, x, y, size, integralImage):
        """
        ------          ------
        |0000|  ------  |0000|
        |0000|  |0000|  |0000|
        ------  ------  -----
        |1111|  |1111|  |1111|
        |1111|  |1111|  ------
        ------  ------
        """
        if (haar_id != HaarFeatureId.B2HWB):
            raise ValueError("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.B2HWB.name, haar_id.name))
        else:
            assert(size >= 2)
            (a, b) = (size // 2, size % 2)
            firstValue = integralImage.getSubWindow(x, y, size, a)
            secondValue = integralImage.getSubWindow(x, y + a, size, a + b)
            resultSubstraction = firstValue - secondValue
            return resultSubstraction

    def computeHaarC3WBW(haar_id, x, y, size, integralImage):
        """
        ----------  -----------
        |00|11|00|  |00|111|00|
        |00|11|00|  |00|111|00|
        ----------  -----------
        """
        if (haar_id != HaarFeatureId.C3WBW):
            raise ValueError("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.C3WBW.name, haar_id.name))
        else:
            assert(size >= 3)
            h = size
            (a, b) = (size // 3, size % 3)
            (x0, w0) = (x, a)
            (x1, w1) = (x + w0, w0 + b)
            x2 = x1 + a

            firstValue = integralImage.getSubWindow(x0, y, w0, h)
            secondValue = integralImage.getSubWindow(x1, y, w1, h)
            thirdValue = integralImage.getSubWindow(x2, y, w0, h)

            resultSubstraction = firstValue + thirdValue - secondValue
            return resultSubstraction

    def computeHaarD4WBBW(haar_id, x, y, size, integralImage):
        """
        -------  --------  --------
        |00|11|  |00|111|  |000|11|
        -------  --------  --------
        |11|00|  |11|000|  |111|00|
        -------  --------  --------
        """
        if (haar_id != HaarFeatureId.D4WBBW):
            raise ValueError("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.D4WBBW.name, haar_id.name))
        else:
            assert(size >= 2)
            (a, b) = (size // 2, size % 2)
            (x0, y0, w0, h0) = (x, y, a, a)
            (x1, y1, w1) = (x + a, y, a + b)
            (y2, h2) = (y + a, a + b)

            firstValue = integralImage.getSubWindow(x0, y0, w0, h0)
            secondValue = integralImage.getSubWindow(x1, y1, w1, h0)
            thirdValue = integralImage.getSubWindow(x0, y2, w0, h2)
            fourthValue = integralImage.getSubWindow(x1, y2, w1, h2)

            resultSubstraction = firstValue + fourthValue - (secondValue + thirdValue)
            return resultSubstraction

    def __str__(self):
        return ("haar_id = %s\nis_inverted = %s\n" % (self.haar_id.name, self.is_inverted))
