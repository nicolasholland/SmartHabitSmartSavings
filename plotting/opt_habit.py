import os
import sys
import time
import csv
import math
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
        ret += (R[ind] - C[ind])**2

    return math.sqrt(ret)

def super_simple_optimization(C, step=0):
    """ Optimizes the behaivour in the simplest way possible.
        (Moves it towards the evening.)
    """
    ret = np.zeros(len(C))

    for i in xrange(0, len(C)-step - 1):
        if i >= 97 or i + step >= 97:
            continue
        ret[i] = C[i + step]

    for i in xrange(0, step):
        ret[len(C) - step - 1 + i] = C[i]

    return ret

def actual_optimization(R, C, start=-50, stepwidth=1, maxrange=50):
    """ This function actually does some optimization.
        (Looking at you super_simple_optimization)

    Parameters
    ----------
    R : ndarray
        renewable energy production
    C : ndarray
        Household energy consumption
    start : int
        define interval for parameter search
    stepwidth : int
        define stepwidth for parameter search
    maxrange : int
        define interval for parameter search

    Returns
    -------
    best_step : int
        optimal parameter for super_simple_optimization
    minval : float
    """
    minval = target_function(R, C)
    best_step = 0

    for step in xrange(start, maxrange, stepwidth):
        oc = super_simple_optimization(C, step=step)
        val = target_function(R, oc)

        print("%d %d %d %f"%(step, start, maxrange, val))

        if val < minval:
            minval = val
            best_step = step

    return best_step, minval

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
    consum = consum / (1000000) * 10000
    day_data_set.append(consum)

    diff = target_function(day_data_set[2], day_data_set[3])

    print("||R-C|| = ", diff)

    step, val = actual_optimization(day_data_set[2], day_data_set[3])

    print("Optimal step: ", step)
    print("||R-OC|| = ", val)


def get_difference(nofhouseholds, opt_param,
                   house_fn=("/home/dutchman/Daten/debs_challenge_2014/"
                             "debs_0_0.csv"),
                   date="01.09.2013"):
    """ Helper function to compute difference between habits.

    Parameters
    ----------
    nofhouseholds : int
    opt_param : int
    date : string
        Default 01.09.2013
    """
    day_data_set = []
    # Wind
    data = read_data.read_csv(("/home/dutchman/Daten/2013_energy_feed_in/"
                               "Windenergie_Hochrechnung_2013.csv"),
                               skip=5)
    day_data = daily_production.get_one_day(data, date,
                                            date_pos=0, data_pos=3,
                                            mult=1000)
    day_data_set.append(day_data)

    # Solar
    data = read_data.read_csv(("/home/dutchman/Daten/2013_energy_feed_in/"
                               "Solarenergie_Hochrechnung_2013.csv"),
                              skip=5)
    day_data = daily_production.get_one_day(data, date, date_pos=0,
                                            data_pos=3)
    day_data_set.append(day_data)

    # Renewable
    day_data = day_data_set[0] + day_data_set[1]
    day_data_set.append(day_data)

    # Household 
    #house_fn = ("/home/dutchman/Daten/debs_challenge_2014/"
    #            "debs_0_0.csv")
    consum = accumulate.accumulate_household(house_fn)
    consum = consum / (1000000) * nofhouseholds

    consum = super_simple_optimization(consum, step=opt_param)

    day_data_set.append(consum)
    diff = target_function(day_data_set[2], day_data_set[3])

    return diff


if __name__ == '__main__':
    consumption_production()



