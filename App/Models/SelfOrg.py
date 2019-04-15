# For voxel floor func
import math

# For instance testing
from Cell import Cell

import Turtle

# SHADOW PARAMETERS ------------------------------------------------------------
num_voxels      = 20# 100
shadow_width    = 6# 10
shadow_height   = 2# 10
dec_at_0        = 0.99# 0.95
dec_at_1        = 1# 0.99
# ------------------------------------------------------------------------------


# HELPERS ----------------------------------------------------------------------
voxel_width     = 4.5 / num_voxels
voxels          = [[[]]]
diff            = dec_at_1 - dec_at_0
max_ijk         = 2*shadow_width + shadow_height

def dec(i,j,k):
    x = abs(i) + abs(j) + abs(k)
    return dec_at_0 + diff*x/max_ijk

def what_box(x,y,z):
    vx = min(max(int(math.floor((2+x)/voxel_width)),0),num_voxels-1)
    vy = min(max(int(math.floor((2+y)/voxel_width)),0),num_voxels-1)
    vz = min(max(int(math.floor((2+z)/voxel_width)),0),num_voxels-1)
    return (vx,vy,vz)

# Propogate in pyramid
def dec_prop(x,y,z):
    global voxels
    ix,iy,iz = what_box(x,y,z)
    for j in range(0,shadow_height):
        for k in range(-j,j+1):
            for i in range(-j,j+1):
                a = min(max(ix+i,0),num_voxels-1)
                b = min(max(iy-j,0),num_voxels-1)
                c = min(max(iz+k,0),num_voxels-1)
                voxels[a][b][c] *= dec(i,j,k)
                #if (voxels[a][b][c]==0):
                    #print(a,b,c)
# END shadow set up ------------------------------------------------------------


def calc_light(vertices,   # ---------------------------------------------------
               in_num_voxels,
               in_shadow_height,
               in_shadow_width,
               in_decrement_close,
               in_decrement_far):

    # update global params
    global num_voxels, shadow_height_, shadow_width, dec_at_0, dec_at_1
    num_voxels      = in_num_voxels
    shadow_height   = in_shadow_height
    shadow_width    = in_shadow_width
    dec_at_0        = in_decrement_close
    dec_at_1        = in_decrement_far

    global voxels # to allow dec_prop to access
    voxels = [[[1 for k in range(num_voxels)] for j in range(num_voxels)] for i in range(num_voxels)]

    for p in vertices[::2]:
        (x,y,z) = p[:3]
        dec_prop(x,y,z)

    return voxels
# END CALC LIGHT ---------------------------------------------------------------


def update_cells(tree, voxels, scale): # -----------------------------------
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
            xyzr = turtle.View(False)
            (x,y,z) = xyzr[:3]
            x /= scale
            y /= scale
            z /= scale
            ix,iy,iz = what_box(x,y,z)
            try:
                lightvalue = voxels[ix][iy][iz]
            except:
                print(ix,iy,iz)
                raise Exception(ix,iy,iz)
            element.can_i_grow = lightvalue

        elif element == "[":
            stack.append(turtle)
            turtle = turtle.New()
        elif element == "]":
            turtle = stack.pop()
        else:
            turtle.Interpret(element)
# END SHADOW PROP # --------------------------------------------------------
