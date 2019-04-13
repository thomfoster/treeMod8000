# For voxel floor func
import math

# For instance testing
from Cell import Cell

import Turtle

from Interpreter import scale

# SHADOW PARAMETERS ------------------------------------------------------------
num_voxels      = 50# 100
shadow_width    = 4# 10
shadow_height   = 20# 10
dec_at_0        = 0.95# 0.95
dec_at_1        = 1# 0.99
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
        for k in range(-j,j+1):
            for i in range(-j,j+1):
                a = min(max(ix+i,0),num_voxels-1)
                b = min(max(iy-j,0),num_voxels-1)
                c = min(max(iz+k,0),num_voxels-1)
                voxels[a][b][c] *= dec(i,j,k)
                if (voxels[a][b][c]==0):
                    print(a,b,c)
# END shadow set up ------------------------------------------------------------

def calc_light(points):

    global voxels # to allow dec_prop to access
    voxels = [[[1 for k in range(num_voxels)] for j in range(num_voxels)] for i in range(num_voxels)]

    for p in points[::2]:
        (x,y,z) = p[:3]
        dec_prop(x,y,z)

    return voxels

# for i in range(0, num_voxels):
#     for j in range(0, num_voxels):
#         for k in range(0, num_voxels):
#             x = voxels[i][j][k]
#             # print(x)

def update_cells(tree, light_data):

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
            lightvalue = light_data[ix][iy][iz]
            element.can_i_grow = lightvalue

        elif element == "[":
            stack.append(turtle)
            turtle = turtle.New()
        elif element == "]":
            turtle = stack.pop()
        else:
            turtle.Interpret(element)
# END shadow prop # --------------------------------------------------------
