import numpy as np
from math import sqrt, pow, pi, cos, sin

def find_perp(v):
        if (v[0] == 0) and (v[1] == 0):
            if (v[2] == 0):
                raise ValueError("Cant compute perp of 0 vector")
            return [0,1,0]
        return [-v[1], v[0], 0]

def normalise(v):
    mag = pow(v[0],2) + pow(v[1],2) + pow(v[2],2)
    return [x/mag for x in v]

def cutoff(x):
    if abs(x) < pow(10, -10):
        return 0
    return x

def generate_points(p1, p2, r, n):
    u = [y-x for (x,y) in zip(p1,p2)]
    v = find_perp(u)
    z = np.cross(u,v)

    v = normalise(v)
    z = normalise(z)

    ang = 0
    points = []
    for i in range(0,n):
        ang = i*2*pi/n
        c = cos(ang)
        s = sin(ang)
        p = [ cutoff(p + r*x*c + r*y*s) for (p,x,y) in zip(p1,v,z)]
        points.append(p)
    return points
