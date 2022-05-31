#!/usr/bin/env python3
# This script is a rewritten version of the pendula scripts
# modified in a way that the top particle has fixed Y coordinate.
# Update (2022): simplify code for a standard pendulum
#
# Requirements
# ============
#
#  - python3
#  - matplotlib
#  - numpy
# On most of the modern Linux distros (including Slackware) python3 is
# a part of base system. To install python libraries either use your package
# manager, or use ``pip3'' command (namely, `pip3 install matplotlib` and so
# on). MacOS users should also have python3 (and pip3) installed.
# 
# Execution
# =========
# Type `python3 sliding_pendulum.py` in your GUI Terminal. A new window with
# animation should appear on your screen automatically, if everything is
# fine.
#
# Copyright (c) 2021 Andrei Rabusov
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

v=0.8
alpha=10*np.pi/180.
L = 1.0
l = -0.4 * L
R=0.05

# Theoretical prediction:
#                2 R cos (phi)
# tan alpha = ------------------
#              l - 2 R sin (phi)
# Which is obviously wrong if phi = 0
# phi can't be less then alpha

M1 = 1.0  # mass of the first particle (fixed on the X axis)
M2 = 1.0  # mass of the second particle, the bottom end of the pendulum
t_stop = 1.3  # how many seconds to simulate
history_len = 5000  # how many trajectory points to display

fmt='{:.2f}'
def collide (p1, p2, beta):
    c, s = np.cos(beta), np.sin(beta)
    R=np.array (((c, -s), (s, c)))
    RT=np.array (((c, s), (-s, c)))
    p1p = R.dot (p1)
    p2p = R.dot (p2)
    p1p[1], p2p [1] = p2p [1], p1p [1]
    return RT.dot(p1p), RT.dot(p2p)

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)

def derivs(state, t):

    dydx = np.zeros_like(state)

    dist2 = (state[0]-state[4])**2 + (state[1]-state[5])**2
    dist2n = (state[0]+dt*(state[2]-state[6])-state[4])**2
    + (state[1]+dt*(state[3]-state[7])-state[5])**2
    if (dist2n <= 4*R**2) and (dist2 >= 4*R**2):
        beta = np.arctan2(state[1]-state[5], state[0]-state[4])
        p1, p2 = collide (M1*np.array ([state[2], state[3]]),
                M2*np.array ([state[6], state[7]]), np.pi/2-beta)
        state[2] = p1 [0]/M1
        state[3] = p1 [1]/M1
        state[6] = p2 [0]/M2
        state[7] = p2 [1]/M2
        print ('initial angle =', fmt.format (alpha*180/np.pi)+' [deg]')
        print ('scattering angle =', fmt.format (np.arctan2 (p2[1],
            p2[0])*180/np.pi)+' [deg]')

    dydx[0] = state[2]
    dydx[1] = state[3]
    dydx[4] = state[6]
    dydx[5] = state[7]
    # F = ma for the first particle

    return dydx

# initial state
# State is 1D array, even components are coordinates, odd --- velocities
# Now multiply by two (2D problem)
state = [l, 0, v*np.cos(alpha),v*np.sin(alpha), 0,0, 0,0]

y = np.zeros ((np.size (t), np.size(state)))
y[0] = state
for i, titem in enumerate (t):
    if i > 0:
        y[i] = derivs (y [i-1], titem)*dt + y [i-1]

# Unpack results
x1 = y[:, 0]
y1 = y[:, 1]
x2 = y[:, 4]
y2 = y[:, 5]


fig = plt.figure(figsize=(8, 6))
# Here you can adjust the size of the window and the limits.
ax = fig.add_subplot(autoscale_on=False, xlim=(-0.7*L, 0.4*L),
        ylim=(-0.5*L, 0.5*L))
# Pay attention, that the aspect ratio is 1
ax.set_aspect('equal')
ax.grid()

line1, = ax.plot([], [], '-', lw=2)
line2, = ax.plot([], [], '-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

phis = np.arange (0, 2*np.pi+np.pi/9, np.pi/9)
def circle (x, y, r):
    return r*np.cos (phis) + x, r*np.sin (phis) + y,

def animate(i):
    thisx1, thisy1 = circle (x1[i], y1[i], R) 
    thisx2, thisy2 = circle (x2[i], y2[i], R) 

    line1.set_data(thisx1, thisy1)
    line2.set_data(thisx2, thisy2)

    time_text.set_text(time_template % (i*dt))
    return line1, line2, time_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
plt.show()
