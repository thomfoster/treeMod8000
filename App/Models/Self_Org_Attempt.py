# Voxel based shadow propogation -------------------------------------------
# Updates cell probabilities based on what we just learned

num_voxels      = 100
shadow_width    = 10
shadow_height   = 10
dec_at_0        = 0.2
dec_at_1        = 0.6
impact          = 1

# Create 3D array of cells all with light value 1
voxel_width     = 2 / 100
voxels          = [[[1 for k in range(num_voxels)] for j in range(num_voxels)] for i in range(num_voxels)]

# Linear shadow propogation
diff            = dec_at_1 - dec_at_0
max_ijk         = 2*shadow_width + shadow_height
def dec(i,j,k):
    x = i + j + k
    return dec_at_0 + diff*x/max_ijk

def what_box(x,y,z):
    vx = int(math.floor((1+x)/voxel_width))
    vy = int(math.floor((y+1)/voxel_width))
    vz = int(math.floor((z+1)/voxel_width))
    return (vx,vy,vz)

# Propogate in pyramid
def dec_prop(x,y,z):
    ix,iy,iz = what_box(x,y,z)
    for j in range(0,shadow_height):
        for i in range(-j,j+1):
            for k in range(-j,j+1):
                a = min(max(ix+1,0),num_voxels-1)
                b = min(max(iy+1,0),num_voxels-1)
                c = min(max(iz+1,0),num_voxels-1)
                voxels[a][b][c] *= dec(i,j,k)

# CALCULATE VOXEL VALUES
for p in points[::2]:
    (x,y,z) = p[:3]
    dec_prop(x,y,z)

# UPDATE CELL PROBABILITIES
# Iterate over cells again
points = []
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
        print(x,y,z)
        # ix,iy,iz = what_box(x,y,z)
        # lightvalue = voxels[ix][iy][iz]
        # element.can_i_grow = lightvalue

    elif element == "[":
        stack.append(turtle)
        turtle = turtle.New()
    elif element == "]":
        turtle = stack.pop()
    else:
        turtle.Interpret(element)
# END shadow prop # --------------------------------------------------------
