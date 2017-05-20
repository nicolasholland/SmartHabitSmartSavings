import os
import sys
import time
import csv
import numpy as np

sys.path.append('../io/')
import read_data 
import accumulate
import daily_production

def target_function(R, C):
    """ Target function that we want to minimize.

    Parameters
    ----------
    R : ndarray
        Supposed to be the renewable energy production.
    C : ndarray
        Supposed to be the energy consumption for n households.

    Notes
    -----
    We want to minimize the difference between the two arrays.
    That should minimize the amount of conventional energy.
    """
    ret = 0

    for ind in xrange(len(R)):
        ret += abs(R[ind] - C[ind])

    return ret

def super_simple_optimization(C, step=0):
    """ Optimizes the behaivour in the simplest way possible.
        (Moves it towards the evening.)
    """
    ret = np.zeros(len(C))

    for i in xrange(0, len(C)-step):
        ret[i] = C[i + step]

    for i in xrange(0, step):
        ret[len(C) - step + i] = C[i]

    return ret

def consumption_production():
    """ Compare renewable energy production with energy consumption.
    """
    day_data_set = []
    # Wind
    data = read_data.read_csv(("/home/dutchman/Daten/2013_energy_feed_in/"
                               "Windenergie_Hochrechnung_2013.csv"),
                               skip=5)
    day_data = daily_production.get_one_day(data, sys.argv[1],
                                            date_pos=0, data_pos=3,
                                            mult=1000)
    day_data_set.append(day_data)

    # Solar
    data = read_data.read_csv(("/home/dutchman/Daten/2013_energy_feed_in/"
                               "Solarenergie_Hochrechnung_2013.csv"),
                              skip=5)
    day_data = daily_production.get_one_day(data, sys.argv[1], date_pos=0,
                                            data_pos=3)
    day_data_set.append(day_data)

    # Renewable
    day_data = day_data_set[0] + day_data_set[1]
    day_data_set.append(day_data)

    # Household 
    house_fn = ("/home/dutchman/Daten/debs_challenge_2014/"
                "debs_0_0.csv")
    consum = accumulate.accumulate_household(house_fn)
    consum = consum / (1000000) * 1
    day_data_set.append(consum)

    diff = target_function(day_data_set[2], day_data_set[3])

    print("||R-C|| = ", diff)


if __name__ == '__main__':
    consumption_production()



