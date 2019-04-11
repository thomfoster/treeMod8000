import math
import numpy as np
from numpy import dot
from numpy.linalg import inv

# ------------------------------------------------------------------------------
# Provides the do_rot function thats used to rotate the turtle
# WARNING / TODO: Stop using numpy matrices and doing this manually - very slow
# ------------------------------------------------------------------------------

def mag(vec):
    sum = 0
    for i in vec:
        sum += math.pow(i,2)
    return math.sqrt(sum)

def angleBetween(vec1, vec2):
    # Misleading name:
    #   If vec1 is [1,0,0] we project vec2 into xz plane and calc angle
    #   If vec1 is [0,1,0] we just calculate angle
    # Returns angle in [0,180].
    # If we're comparing to x axis - I want it to return in [0, 360]
    # With angle in [180,360] if z value less than 0

    if np.array_equal([1,0,0], vec1):
        vec1 = [1,0]
        vec2 = [vec2[0], vec2[2]]

    ang = dot(vec1, vec2) / (mag(vec1)*mag(vec2))
    ang = min(ang, 1)
    ang = max(ang, -1)

    if vec1 == [1,0]:
        if vec2[1] < 0:
            return 360 - math.degrees(math.acos(ang))
    return math.degrees(math.acos(ang))

# create rotation matrix to rotate axis = (u,v,w) about the z axis to the xz plane
# could do with getting these sqrts removed too
def t_xz(axis):
    u = axis[0]
    v = axis[1]
    sqrt = math.sqrt(math.pow(u,2)+math.pow(v,2))
    return np.array([
        u/sqrt, v/sqrt, 0,
        -v/sqrt, u/sqrt, 0,
        0, 0, 1,
    ]).reshape(3,3)

# create rotation matrix to rotate axis = (u,v,w) about the y so that vector now
# is aligned with z axis
def t_z(axis):
    u = axis[0]
    v = axis[1]
    w = axis[2]
    sqrtl = math.sqrt(math.pow(u,2) + math.pow(v,2) + math.pow(w,2))
    sqrts = math.sqrt(math.pow(u,2) + math.pow(v,2))
    return np.array([
        w/sqrtl, 0, -sqrts/sqrtl,
        0, 1, 0,
        sqrts/sqrtl, 0, w/sqrtl
    ]).reshape(3,3)

# Rotation matrix about z
def r_z(theta):
    return np.array([
        math.cos(theta), -math.sin(theta), 0,
        math.sin(theta), math.cos(theta), 0,
        0,0,1
    ]).reshape(3,3)

def do_rot(S,axis_label,theta_deg):
    theta_rad = math.pi*theta_deg/180
    axis = S[:, axis_label]
    A = t_xz(axis)
    B = t_z(axis)
    R = r_z(theta_rad)
    # At = inv(A)
    # Bt = inv(B) // Using transpose cuts time in half
    At = A.transpose()
    Bt = B.transpose()
    ret = S
    ret = dot(A,ret)
    ret = dot(B,ret)
    ret = dot(R,ret)
    ret = dot(Bt,ret)
    ret = dot(At,ret)
    return ret
