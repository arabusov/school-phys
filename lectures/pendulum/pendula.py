#!/usr/bin/env python3
# This script is C&P from the matplotlib example ``double_pendulum'' and
# modified in a way that the top particle has fixed Y coordinate.
# Update (2022): simplify code for a standard pendulum
#
# Requirements
# ============
#
#  - python3
#  - matplotlib
#  - numpy
#  - scipy
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
import scipy.integrate as integrate
import matplotlib.animation as animation
from collections import deque

G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0
L2 = L1
M1 = 1.0  # mass of the first particle (fixed on the X axis)
M2 = 1.0  # mass of the second particle, the bottom end of the pendulum
t_stop = 5  # how many seconds to simulate
history_len = 5000  # how many trajectory points to display
phi0 = -np.pi/8.

def nonlinear (phi, L):
    return -G*np.sin (phi)/L
def linear (phi, L):
    return -G*phi/L
def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]
    # F = ma for the first particle
    dydx[1] = 0
    dydx[1] = nonlinear (state[0], L1)

    dydx[2] = state[3]

    dydx[3] = nonlinear (state[2], L2)

    return dydx

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)

# x and v --- first (top) particle coordinate and velocity
phi1 = phi0/2
w1 = .0
# phi and w --- angle and angular velocity of the second (bottom) particle
phi2 = phi0
w2 = 0.

# initial state
# State is 1D array, even components are coordinates, odd --- velocities
state = [phi1, w1, phi2, w2]

# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)

# Unpack results
x1 = L1*np.sin(y[:, 0])
y1 = -L1*np.cos(y[:, 0])

# Angle phi must be transformed to the 2D coordinate relative to the first
# particle position (x1, y1)
x2 = L2*np.sin(y[:, 2])
y2 = -L2*np.cos(y[:, 2])

fig = plt.figure(figsize=(12.5, 5))
# Here you can adjust the size of the window and the limits.
ax = fig.add_subplot(autoscale_on=False, xlim=(-1.3*L2, 2.2*L2), ylim=(-1.2*L2, 0.1))
# Pay attention, that the aspect ratio is 1
ax.set_aspect('equal')
ax.grid()

line1, = ax.plot([], [], 'o-', lw=2)
line2, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def animate(i):
    thisx1 = [x1[i], 0]
    thisy1 = [y1[i], 0]
    thisx2 = [x2[i], 0]
    thisy2 = [y2[i], 0]

    line1.set_data(thisx1, thisy1)
    line2.set_data(thisx2, thisy2)

    time_text.set_text(time_template % (i*dt))
    return line1, line2, time_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
plt.show()
