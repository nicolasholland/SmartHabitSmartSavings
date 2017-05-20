import os
import sys
import time
import csv
import math
import numpy as np

import opt_habit

def analytics(nofhouseholds):
    """ Some simple middle school math to analyze our savings.
    """
    # household 0_0

#    dRegularRenewable = 38427.369411931846
#    dOptimizedRenewable = 37141.586356465545
#    dOptimizedDevices = 0

    dRegularRenewable = opt_habit.get_difference(nofhouseholds, 0)
    dOptimizedRenewable = opt_habit.get_difference(nofhouseholds, -12)
    dOptimizedDevices = 0

    one_percent  = dRegularRenewable / 100
    savings = abs(dOptimizedRenewable - dRegularRenewable) / one_percent
    devicesavings = dOptimizedDevices / one_percent

    print("Savings: ", savings)
    print("Device Savings: ", devicesavings)
    
    # household 0_1
    

if __name__ == '__main__':
    analytics(100000)
