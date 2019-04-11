# ------------------------------------------------------------------------------
# String to Points Implementation
# ------------------------------------------------------------------------------
# Parse the derived string, keeping track of the turtles location in space
# This step is closely linked to the actual visualisation so will need to be
# adapted for each example.
# # The approach we take is close to the one we developed in the 2D LSytems.py in
# that we use lambda functions defined inside an interpretation dict to tell the
# turtle what to do.

import sys
import numpy as np
import rotations
import Parser
import Stochastic_L_Systems
import sys
import geometry

dna = Parser.parse("Demos/"+sys.argv[1]+".txt") #Yes i do it twice cuff me
mystr = Stochastic_L_Systems.derive("Demos/"+sys.argv[1]+".txt")
print(mystr)

# ------------------------------------------------------------------------------
# Initialise State dict
# ------------------------------------------------------------------------------

state = {
'position': np.array([0,-1,0]), #Simple 3D Vector coords
'heading': np.eye(3),  #3D orientation vectors. Rotated below so that axis 0 is up
'thickness': 0.1,
'just_popped': False
}

state['heading'] = rotations.do_rot(state['heading'],1,90)
state['heading'] = rotations.do_rot(state['heading'],2,90)

stack = []

length = 0
delta1 = 0
delta2 = 0

def ageToLength(j):
    name, age = j
    return age

def pushTurt():
    newstate = {}
    newstate['position'] = state['position'].view()
    newstate['heading'] = state['heading'].view()
    newstate['thickness'] = state['thickness']
    newstate['just_popped'] = state['just_popped']
    stack.append(newstate)

def popTurt():
    global state
    popped = stack.pop()
    state['position'] = popped['position'].view()
    state['heading'] = popped['heading'].view()
    state['thickness'] = popped['thickness']
    state['just_popped'] = True


def forward(length):
    state['position'] = state['position'] + length*state['heading'][:,0]

def roll(axis_label, theta):
    state['heading'] = rotations.do_rot(state['heading'], axis_label, theta)

def incThickness():
    state['thickness'] = State['thickness'] / 0.9

def decThickness():
    state['thickness']  = state['thickness'] * 0.9
    if state['thickness'] < 0:
        state['thickness'] = system['end_thickness']


interpretation = { # Standard interpretation list
"+": lambda: roll(0,delta1),
"-": lambda: roll(0,-delta1),
"&": lambda: roll(1,delta1),
"^": lambda: roll(1,-delta1),
"?": lambda: roll(2,delta1),
"/": lambda: roll(2,-delta1),
"?": lambda: roll(2,-delta2),
"|": lambda: roll(0,180),
"[": lambda: pushTurt(),
"]": lambda: popTurt(),
"I": lambda: incThickness(),
"D": lambda: decThickness()
}

# For scaling the generated model
mins = [0,0,0]
maxs = [0,0,0]

# Just keeps track of the max and min values its seen in each axis
def updateExtrema(point):
    for i in [0,1,2]:
        if point[i] < mins[i]:
            mins[i] = point[i]
        if point[i] > maxs[i]:
            maxs[i] = point[i]

def plot(ls):
    # Set these before calling lambda function
    global length, delta1, delta2

    n = len(ls)
    print("Model derived of length " + str(n))

    previous = state['position']
    current = state['position']

    # The naming pairs comes the fact that this array of points is interpeted by opengl
    # in groups of two points. Although this seems excessive when the points are successive
    # taking the points sequentially would cause issues when the turtles stack machine
    # causes it to jump from a branch tip back to the centre of the tree
    pairs = []
    # Literally just for progress reporting
    i = 0
    for l in ls:
        i += 1
        sys.stdout.write('\r')
        sys.stdout.write("Converting string to points: "+ str(int(100*i/n))+"%")
        func = None

        # If we're drawing a cell
        if isinstance(l, tuple):
            name, age = l
            delta1 = dna[name]["Angles"][0]
            delta2 = dna[name]["Angles"][1]
            length = ageToLength(l)
            state["thickness"] *= dna[name]["Decay"][0] ** age
            forward(length)

        # If the character has an interpretation, perform it
        else:
            try:
                func = interpretation[chr]
                func()
            except KeyError:
                # Dont throw exception. There are characters that just map to themselves
                # As placeholders for a branch, and have no interpretation
                pass

        # If we've moved add the points to the pairs array
        if not np.array_equal(current, state['position']):
            current, previous = state['position'], current
            updateExtrema(current)
            previousVertexData = (previous[0], previous[1], previous[2], state["thickness"])
            currentVertexData  = (current[0], current[1], current[2], state["thickness"])
            if not state['just_popped']:
                pairs.append(previousVertexData) #Duplicate the previous entry
                pairs.append(currentVertexData)
            else:
                # Next time we move we'll plot the points
                state['just_popped'] = False

    scale = 0.5*max([abs(x-y) for (x,y) in zip(mins, maxs)]) # 0.4 as for some reason a width of 1 is not full width, I think because the points are all shifted back 5 by the view matrix
    print()
    print("Scale factor set at:" + str(scale))
    scaled_points = [(x/scale, y/scale, z/scale, r) for (x,y,z,r) in pairs]
    return scaled_points

# Generate points
points = plot(mystr)

# Apply cutoff filter
def cutoff(i):
    if (abs(i) < 10**(-10)):
        return 0
    return i

points = [(cutoff(x),cutoff(y), cutoff(z), r) for (x,y,z,r) in points]

pairs = zip(points[0::2], points[1::2])

# Write to file
with open("data.dat", mode="w") as f:
    f.write(str(len(points))+"\n")
    for p1, p2 in pairs:
        if p1[3] == 0:
            continue
        for col in p1:
            f.write(str(col)+"\t")
        f.write("\n")
        for col in p2:
            f.write(str(col)+"\t")
        f.write("\n")
