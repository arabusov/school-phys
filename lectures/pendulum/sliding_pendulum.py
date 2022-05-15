#!/usr/bin/env python3
# This script is C&P from the matplotlib example ``double_pendulum'' and
# modified in a way that the top particle has fixed Y coordinate.
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
L = 1.0
M1 = 1.0  # mass of the first particle (fixed on the X axis)
M2 = 1.0  # mass of the second particle, the bottom end of the pendulum
t_stop = 5  # how many seconds to simulate
history_len = 500  # how many trajectory points to display
phi0 = -np.pi/4.

def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]
    # Tension:
    T = M2*(G*np.cos (state[2])+L*state[3]**2)/\
        (1.+M2/M1*np.sin(state[2])**2)
    # F = ma for the first particle
    dydx[1] = 1./M1 * T*np.sin (state[2])

    dydx[2] = state[3]

    dydx[3] = -dydx[1]*np.cos(state[2])/L - G*np.sin(state[2])/L

    return dydx

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.02
t = np.arange(0, t_stop, dt)

# x and v --- first (top) particle coordinate and velocity
x = -0.3
v = .5
# phi and w --- angle and angular velocity of the second (bottom) particle
phi = phi0
w = 0.

# initial state
# State is 1D array, even components are coordinates, odd --- velocities
state = [x, v, phi, w]

# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)

# Unpack results
x1 = y[:, 0]
y1 = np.zeros_like (x1)

# Angle phi must be transformed to the 2D coordinate relative to the first
# particle position (x1, y1)
x2 = L*np.sin(y[:, 2]) + x1
y2 = -L*np.cos(y[:, 2]) + y1

fig = plt.figure(figsize=(12.5, 5))
# Here you can adjust the size of the window and the limits.
ax = fig.add_subplot(autoscale_on=False, xlim=(-1.3*L, 2.2*L), ylim=(-1.2*L, 0.1))
# Pay attention, that the aspect ratio is 1
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], ',-', lw=1)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)


def animate(i):
    thisx = [x1[i], x2[i]]
    thisy = [y1[i], y2[i]]

    if i == 0:
        history_x.clear()
        history_y.clear()

    history_x.appendleft(thisx[1])
    history_y.appendleft(thisy[1])

    line.set_data(thisx, thisy)
    trace.set_data(history_x, history_y)
    time_text.set_text(time_template % (i*dt))
    return line, trace, time_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
plt.show()
