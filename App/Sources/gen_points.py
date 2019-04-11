# ------------------------------------------------------------------------------
# String to Points Implementation
# ------------------------------------------------------------------------------
# Parse the derived string, keeping track of the turtles location in space
# This step is closely linked to the actual visualisation so will need to be
# adapted for each example.
# # The approach we take is close to the one we developed in the 2D LSytems.py in
# that we use lambda functions defined inside an interpretation dict to tell the
# turtle what to do.

import numpy as np
import rotations
import Parser
from Parser import system
import sys
import geometry

state = {
'position': np.array([0,-1,0]), #Simple 3D Vector coords
'heading': np.eye(3)  #3D orientation vectors. Initially rotated so that axis 0 is up
}

state['heading'] = rotations.do_rot(state['heading'],1,90)
state['heading'] = rotations.do_rot(state['heading'],2,90)

print(state['heading'])

stack = []

# Initialisation
length = 0
delta = 0

def pushTurt():
    newstate = {}
    newstate['position'] = state['position'].view()
    newstate['heading'] = state['heading'].view()
    stack.append(newstate)

def popTurt():
    global state
    popped = stack.pop()
    state['position'] = popped['position'].view()
    state['heading'] = popped['heading'].view()


def forward(length):
    state['position'] = state['position'] + length*state['heading'][:,0]

def roll(axis_label, theta):
    state['heading'] = rotations.do_rot(state['heading'], axis_label, theta)

interpretation = { # Standard interpretation list
"R": lambda: forward(length),
"G": lambda: forward(length/50),
"A": lambda: forward(length),
"B": lambda: forward(length),
"C": lambda: forward(length),
"D": lambda: forward(length),
"+": lambda: roll(0,delta),
"-": lambda: roll(0,-delta),
"&": lambda: roll(1,delta),
"^": lambda: roll(1,-delta),
"?": lambda: roll(2,delta),
"/": lambda: roll(2,-delta),
"|": lambda: roll(1,180),
"[": lambda: pushTurt(),
"]": lambda: popTurt()
}

mins = [0,0,0]
maxs = [0,0,0]

def updatemins(point):
    for i in [0,1,2]:
        if point[i] < mins[i]:
            mins[i] = point[i]
        if point[i] > maxs[i]:
            maxs[i] = point[i]

def plot(derived_string):
    global length, delta
    length = system['length']
    delta = system['delta']

    n = len(derived_string)
    print("String derived of length " + str(n))
    previous = state['position']
    current = state['position']
    pairs = []
    i = 0
    for chr in derived_string:
        i += 1
        sys.stdout.write('\r')
        sys.stdout.write("Converting string to points: "+ str(int(100*i/n))+"%")
        func = None
        try:
            func = interpretation[chr]
            func()
        except KeyError:
            pass
        if not np.array_equal(current, state['position']):
            current, previous = state['position'], current
            updatemins(current)
            pairs.append(previous)
            pairs.append(current)

    scale = 0.4* max([abs(x-y) for (x,y) in zip(mins, maxs)]) # 0.4 as for some reason a width of 1 is not full width, I think because the points are all shifted back 5 by the view matrix
    scale = 1
    print()
    print("Scale factor set at:" + str(scale))
    scaled_points = [(x/scale, y/scale, z/scale) for (x,y,z) in pairs]
    extruded_points = []
    print(scaled_points)
    for i in range(1, len(scaled_points)):
        extruded_points += geometry.generate_points(scaled_points[i-1], scaled_points[i], 0.1, 4)
    print(extruded_points)
    return
