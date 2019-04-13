# For % reporting
import sys

# For voxel floor func
import math

# For instance testing
from Cell import Cell

import Turtle

trunkLength = 0 # Make global to allow analyse_model to access this. Hacky :(

# SHADOW PARAMETERS ------------------------------------------------------------
num_voxels      = 100# 100
shadow_width    = 10# 10
shadow_height   = 10# 10
dec_at_0        = 0.95# 0.95
dec_at_1        = 0.99# 0.99
impact          = 1
# ------------------------------------------------------------------------------

# Stuff for shadows ------------------------------------------------------------
voxel_width     = 4.5 / num_voxels
voxels          = [[[]]]
diff            = dec_at_1 - dec_at_0
max_ijk         = 2*shadow_width + shadow_height

def dec(i,j,k):
    x = abs(i) + abs(j) + abs(k)
    return dec_at_0 + diff*x/max_ijk

def what_box(x,y,z):
    vx = int(math.floor((2+x)/voxel_width))
    vy = int(math.floor((y+2)/voxel_width))
    vz = int(math.floor((z+2)/voxel_width))
    return (vx,vy,vz)

# Propogate in pyramid
def dec_prop(x,y,z):
    global voxels
    ix,iy,iz = what_box(x,y,z)
    for j in range(0,shadow_height):
        for i in range(-j,j+1):
            for k in range(-j,j+1):
                a = min(max(ix+i,0),num_voxels-1)
                b = min(max(iy+j,0),num_voxels-1)
                c = min(max(iz+k,0),num_voxels-1)
                voxels[a][b][c] *= dec(i,j,k)
                if (voxels[a][b][c]==0):
                    print(a,b,c)
# END shadow set up ------------------------------------------------------------

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

            # CODE FOR INTERPRETING CELLS HERE ---------------------------------
            # Sets leafs colour in renderer
            leaf = 0;
            if len(element.children)==0:
                leaf = 1

            # Just helps reduce size of data file
            if (turtle.thickness) == 0: # Took out gen limit test
                continue

            turtle.crntCell = element
            updateExtrema(turtle.View()[:3])

            # Plot branch start
            xyzr = turtle.View(return_analysis)
            if return_analysis == True:
                xyzr += (element.Lenth(),)
            xyzr += (float(leaf),)
            points.append(xyzr)

            # Interpret cell
            turtle.Forward(element.Length())
            turtle.Decay()
            updateExtrema(turtle.View()[:3])

            # Plot branch end
            xyzr = turtle.View(return_analysis)
            if return_analysis == True:
                xyzr += (element.Lenth(),)
            xyzr += (float(leaf),)
            points.append(xyzr)

            # For calculating angles
            turtle.parentHeading = turtle.heading[:,0]
            # END CODE FOR INTERPRETING CELLS ----------------------------------

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

    # Scale points to be inside bounding cube of side length 4...
    # ...centered at (0,0,0).
    scale = 0.5 * max([abs(x) for x in (mins+maxs)])
    # print("Scale factor set at: " + str(scale))
    if return_analysis == True:
        points = [(x, y, z, r, verticalAngle, horizontalAngle, parentAngle, length) for (x,y,z,r,l, verticalAngle, horizontalAngle, parentAngle, length) in points]
    else:
        # Just for visuals when rendered, move root to {0,-0.5,0}
        points = [(x/scale, -0.5 + y/scale, z/scale, r/scale, l) for (x,y,z,r,l) in points]


    # Voxel based shadow propogation -------------------------------------------
    # Updates cell probabilities based on what we just learne

    # reset voxels
    global voxels
    voxels = [[[1 for k in range(num_voxels)] for j in range(num_voxels)] for i in range(num_voxels)]

    # CALCULATE VOXEL VALUES
    for p in points[::2]:
        (x,y,z) = p[:3]
        dec_prop(x,y,z)

    for i in range(0, num_voxels):
        for j in range(0, num_voxels):
            for k in range(0, num_voxels):
                x = voxels[i][j][k]
                # print(x)

    # UPDATE CELL PROBABILITIES
    # Iterate over cells again
    stack  = []

    # Instantiate turtle
    turtle = Turtle.Turtle(tree[0])
    turtle.thickness = tree[0].width

    # Traverse structure
    for element in tree:
        if isinstance(element, Cell):
            # No shadow if 0!
            if (turtle.thickness) == 0:
                continue
            turtle.crntCell = element
            # Interpret cell
            turtle.Forward(element.Length())
            turtle.Decay()
            updateExtrema(turtle.View()[:3])
            xyzr = turtle.View(return_analysis)
            (x,y,z) = xyzr[:3]
            x /= scale
            y /= scale
            z /= scale
            ix,iy,iz = what_box(x,y,z)
            lightvalue = voxels[ix][iy][iz]
            element.can_i_grow = lightvalue

        elif element == "[":
            stack.append(turtle)
            turtle = turtle.New()
        elif element == "]":
            turtle = stack.pop()
        else:
            turtle.Interpret(element)
    # END shadow prop # --------------------------------------------------------

    return points
# END INTERPRET ----------------------------------------------------------------
