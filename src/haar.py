#!/usr/bin/env python3

from enum import Enum
import operator
import typing

class HaarFeatureId(Enum):
    A2VWB = 1   # -> 01
    B2HWB = 2   # -> 0/1
    C3WBW = 3   # -> 010
    D4WBBW = 4  # -> 01/10

class Haar(object):
    def __init__(self, haar_id, is_inverted):
        self.haar_id = haar_id
        self.is_inverted = is_inverted

    # The proper way to test constructor arguments
    haar_id = property(operator.attrgetter('_haar_id'))

    @haar_id.setter
    def haar_id(self, haar_id):
        if not haar_id or not isinstance(haar_id, HaarFeatureId):
            raise Exception("haar_id should be one of the HaarFeatureId class values")
        self._haar_id = haar_id

    is_inverted = property(operator.attrgetter('_is_inverted'))

    @is_inverted.setter
    def is_inverted(self, is_inverted):
        if not isinstance(is_inverted, bool):
            raise Exception("is_inverted should be True or False")
        self._is_inverted = is_inverted

    def computeHaar(self, x, y, size, integralImage):
        #TODO implment visitor design pattern so that you will not need to check what method you want to call
        """
        **locals() gives all the local variables: x, y ...
        => you should not declare variables before using it if you need only to pass function arguments
        """
        return {
                HaarFeatureId.A2VWB: computeHaarA2VWB(**locals()),
                HaarFeatureId.B2HWB: computeHaarB2HWB(**locals()),
                HaarFeatureId.C3WBW: computeHaarC3WBW(**locals()),
                HaarFeatureId.D4WBBW: computeHaarD4WBBW(**locals())
                }[haar_id]

    def computeHaarA2VWB(self, haar_id, x, y, size, integralImage):
        """
        -------  --------  --------
        |00|11|  |00|111|  |000|11|
        |00|11|  |00|111|  |000|11|
        -------  --------  --------
        """
        if (haar_id != HaarFeatureId.A2VWB):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.A2VWB.name, haar_id.name))
        else:

            pass

    def computeHaarB2HWB(self, haar_id, x, y, size, integralImage):
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
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.B2HWB.name, haar_id.name))
        else:
            pass

    def computeHaarC3WBW(self, haar_id, x, y, size, integralImage):
        """
        ----------  -----------
        |00|11|00|  |00|111|00|
        |00|11|00|  |00|111|00|
        ----------  -----------
        """
        if (haar_id != HaarFeatureId.C3WBW):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.C3WBW.name, haar_id.name))
        else:
            pass

    def computeHaarD4WBBW(self, haar_id, x, y, size, integralImage):
        """
        -------  --------  --------
        |00|11|  |00|111|  |000|11|
        -------  --------  --------
        |11|00|  |11|000|  |111|00|
        -------  --------  --------
        """
        if (haar_id != HaarFeatureId.D4WBBW):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.D4WBBW.name, haar_id.name))
        else:
            pass


