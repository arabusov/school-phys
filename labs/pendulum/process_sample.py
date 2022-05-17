#!/usr/bin/env python3
import pandas
import numpy as np
import sys

fmt = "{:.4f}"
length = 59 # [cm]
dlength = 0#2
length *= 1./100. # [m]
dlength *= 1./100. # [m]

def eval_gravity (time, length):
    ''' Known that T = 2 pi sqrt (L/g)
    Thus we take T**2 = 4 pi**2 L/g
    g = 4 pi**2 L / T**2
    '''
    return 4. * np.pi**2 * length / time**2
def eval_stddev_gravity (time, dtime, length, dlength):
    dl = dlength / time**2.
    dt = length/time**3 * dtime * (-2)
    return np.sqrt (dl**2 + dt**2) * 4. * np.pi**4
if __name__ == "__main__":
    df = pandas.read_csv (sys.argv[1], escapechar='#',
            skipinitialspace=True)
    time = df['time']/df['nattempts']
    print (time)
    av_time = time.mean ()
    stddev_time = time.std ()
    print ('Average:', fmt.format(av_time), '[s]')
    print ('Stddev: ', fmt.format (stddev_time), '[s]')
    
    g = eval_gravity (av_time, length)
    dg = eval_stddev_gravity (av_time, stddev_time, length, dlength)
    print ('Gravity:', fmt.format (g), '[m/s**2]')
    print ('Gr RMS: ', fmt.format (dg), '[m/s**2]')
