#!/usr/bin/env python3

from enum import Enum
import operator

class HaarFeatureId(Enum):
    A2VWB = 1   # -> 01
    B2HWB = 2   # -> 0/1
    C3WBW = 3   # -> 010
    D4WBBW = 4  # -> 01/10

class Haar(object):
    def __init__(self, haar_id, size):
        self.haar_id = haar_id
        self.size = size

    # The proper way to test constructor arguments
    haar_id = property(operator.attrgetter('_haar_id'))

    @haar_id.setter
    def haar_id(self, haar_id):
        if not haar_id or not isinstance(haar_id, HaarFeatureId):
            raise Exception("haar_id should be one of the HaarFeatureId class values")
        self._haar_id = haar_id

    def computeHaar(self, x, y, integralImage):
        #TODO implment visitor design pattern so that you will not need to check what method you want to call
        """
        **locals() gives all the local variables: x, y ... => you should not declare variables if you need
        only to pass function arguments
        """
        return {
                HaarFeatureId.A2VWB: computeHaarA2VWB(**locals()),
                HaarFeatureId.B2HWB: computeHaarB2HWB(**locals()),
                HaarFeatureId.C3WBW: computeHaarC3WBW(**locals()),
                HaarFeatureId.D4WBBW: computeHaarD4WBBW(**locals())
                }[haar_id]

    def computeHaarA2VWB(self, haar_id, x, y, integralImage):
        if (haar_id != HaarFeatureId.A2VWB):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.A2VWB.name, haar_id.name))
        else:
            pass

    def computeHaarB2HWB(self, haar_id, x, y, integralImage):
        if (haar_id != HaarFeatureId.B2HWB):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.B2HWB.name, haar_id.name))
        else:
            pass

    def computeHaarC3WBW(self, haar_id, x, y, integralImage):
        if (haar_id != HaarFeatureId.C3WBW):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.C3WBW.name, haar_id.name))
        else:
            pass

    def computeHaarD4WBBW(self, haar_id, x, y, integralImage):
        if (haar_id != HaarFeatureId.D4WBBW):
            raise Exception("Invalid Haar computation, expected: %s, found: %s." % (HaarFeatureId.D4WBBW.name, haar_id.name))
        else:
            pass


