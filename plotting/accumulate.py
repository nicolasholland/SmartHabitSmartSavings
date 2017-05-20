import os
import sys
import time
import csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../io/')
import read_data

def hhmm_to_slot(hh, mm):
    return 0

def accumulate_household(filename):
    data = read_data.read_csv(filename,delimiter=",")

    ret = np.zeros(96)
    for point in data:
        tt = read_data.epoch_to_datetime(int(point[1]))

        hh = tt.tm_hour
        mm = tt.tm_min

        slot = hhmm_to_slot(hh, mm)

        #print(float(point[2]))
        ret[slot] += float(point[2])

    return ret

def total_consumption(consumption):
    return consumption.sum()

if __name__ == '__main__':
    accumulate_household(sys.argv[1])    
