# For % reporting
import sys

# For instance testing
from Cell import Cell

import Turtle

trunkLength = 0 # Make global to allow analyse_model to access this. Hacky :(

def interpret(tree, return_analysis=False): # ----------------------------------

    # Accumulating values
    points = []
    stack  = []

    # Final model is scaled to bounding cube with side length = 2
    # Centre of cube at (0,0,0) means model in view.
    # For keeping track of extrema to scale the generated model.
    mins = [0,0,0]
    maxs = [0,0,0]

    # Instantiate turtle
    turtle = Turtle.Turtle(tree[0])
    turtle.thickness = tree[0].width

    # Keeps track of the max and min values its seen in each axis
    def updateExtrema(point):
        for i in [0,1,2]:
            if point[i] < mins[i]:
                mins[i] = point[i]
            if point[i] > maxs[i]:
                maxs[i] = point[i]

    # For printing a progress counter
    i_progress = 0
    n_progress = len(tree)

    # Use the global trunkLength and not an 'in function' local copy
    global trunkLength

    # Traverse structure
    for element in tree:
        if isinstance(element, Cell):
            if (turtle.thickness) == 0: # Took out gen limit test
                continue
            turtle.crntCell = element
            updateExtrema(turtle.View()[:3])
            if return_analysis == True:
                points.append(turtle.View(return_analysis)+(element.Length(),))
            else:
                points.append(turtle.View(return_analysis))
            turtle.Forward(element.Length())
            turtle.Decay()
            updateExtrema(turtle.View()[:3])
            if return_analysis == True:
                points.append(turtle.View(return_analysis)+(element.Length(),))
            else:
                points.append(turtle.View(return_analysis))
            turtle.parentHeading = turtle.heading[:,0] # For calculating angles
        elif element == "[":
            stack.append(turtle)
            # The way objects are represented in memory, any changes to turtle
            # would have also changed the turtle on the stack.
            turtle = turtle.New()
        elif element == "]":
            turtle = stack.pop()
        else:
            turtle.Interpret(element)

        #Print progress
        # i += 1/n
        # sys.stdout.write('\r')
        # sys.stdout.write("Converting string to points: "+ str(int(100*i))+"%")


    # New line for printing after progress counter
    # sys.stdout.write('\n')

    # Find the length until first branch, for metrics.
    trunkLength = 0
    for element in tree:
        if isinstance(element, Cell):
            trunkLength += element.Length()
        elif element == '[':
            break

    # Scale points to be inside bounding cube of side length 2...
    # ...centered at (0,0,0).
    scale = 0.5 * max([abs(x) for x in (mins+maxs)])
    # print("Scale factor set at: " + str(scale))
    if return_analysis == True:
        points = [(x, y, z, r, verticalAngle, horizontalAngle, parentAngle, length) for (x,y,z,r, verticalAngle, horizontalAngle, parentAngle, length) in points]
    else:
        # Just for visuals when rendered, move root to {0,-0.5,0}
        points = [(x/scale, -0.5 + y/scale, z/scale, r/scale) for (x,y,z,r) in points]

    return points
# END INTERPRET ----------------------------------------------------------------
