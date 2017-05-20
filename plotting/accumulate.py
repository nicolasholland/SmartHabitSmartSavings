import os
import sys
import time
import csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../io/')
import read_data
import time_slots

def accumulate_household(filename):
    data = read_data.read_csv(filename,delimiter=",")

    ret = np.zeros(97)
    divisors = np.zeros(97)
    for point in data:
        tt = read_data.epoch_to_datetime(int(point[1]))

        hh = tt.tm_hour
        mm = tt.tm_min

        slot = time_slots.time_to_slot(hh, mm)

        #print(float(point[2]))
        ret[slot] += float(point[2])
        divisors[slot] += 1.

    for slot in xrange(len(ret)):
        if divisors[slot] < 1:
            divisors[slot] = 1
        ret[slot] /= divisors[slot]

    return ret

def total_consumption(consumption):
    return consumption.sum()

if __name__ == '__main__':
    accumulate_household(sys.argv[1])    
