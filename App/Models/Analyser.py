import Interpreter
import math

class movingAverage:
    def __init__(self):
        self.sum = 0
        self.squares = 0
        self.n = 0

    def add(self, x):
        self.sum += x
        self.squares += x**2
        self.n += 1

    def mean(self):
        return self.sum / self.n

    def sd(self):
        return math.sqrt((self.squares/self.n) - self.mean()**2)

class boundingBox:
    def __init__(self):
        self.mins = [1e200,1e200,1e200]
        self.maxs = [-1e200,-1e200,-1e200]

    def add(self, point):
        r = point[3]
        for i in [0,1,2]:
            if point[i]-r < self.mins[i]:
                self.mins[i] = point[i]-r
            if point[i]+r > self.maxs[i]:
                self.maxs[i] = point[i]+r

    def box(self):
        return (self.maxs[0]-self.mins[0], self.maxs[1]-self.mins[1], self.maxs[2]-self.mins[2])

def volumeOfConic(r1, r2, l):
    return (1/3)*math.pi*l*((r2**2) + (r1*r2) + (r1**2))

def analyse(treeData):

    height = -0.5
    for l in treeData:
        height = max(l[1], height)

    n = len(treeData)

    # Take thirds of height
    q1 = 1*math.floor(height/3)
    q2 = 2*math.floor(height/3)

    vOrient = movingAverage()
    hOrient = movingAverage()
    pAng = movingAverage()
    length = movingAverage()
    q1BB = boundingBox()
    q2BB = boundingBox()
    q3BB = boundingBox()
    BB = boundingBox()

    volume = 0

    for i in range(1,n,2):

        (x1, y1, z1, r1, vA, hA, pA, l) = treeData[i-1]
        (x2, y2, z2, r2, vA, hA, pA, l) = treeData[i]

        vOrient.add(vA)
        hOrient.add(hA)
        pAng.add(pA)
        length.add(l)

        p1 = (x1,y1,z1,r1)
        p2 = (x2,y2,z2,r2)

        if y1 < q1:
            q1BB.add(p1)
        elif y1 < q2:
            q2BB.add(p1)
        else:
            q3BB.add(p1)

        if y2 < q1:
            q1BB.add(p2)
        elif y2 < q2:
            q2BB.add(p2)
        else:
            q3BB.add(p2)

        BB.add(p1)
        BB.add(p2)

        volume += volumeOfConic(r1, r2, l)

    stats = {
        'parentAngle_mean': pAng.mean(),
        'parentAngle_variance': pAng.sd(),
        'length_mean': length.mean(),
        'length_variance': length.sd(),
        'verticalOrientation_mean': vOrient.mean(),
        'verticalOrientation_variance': vOrient.sd(),
        'horizontalOrientation_mean': hOrient.mean(),
        'horizontalOrientation_variance': hOrient.sd(),
        'q1_xyz': q1BB.box(),
        'q2_xyz': q2BB.box(),
        'q3_xyz': q3BB.box(),
        'xyz':    BB.box(),
        'trunk_length': Interpreter.trunkLength,
        'totalBiomass': volume,
    }
    return stats

def distance(summaryStats1, summaryStats2):

    # First attempt - Sum of percentage differences
    def percentDiff(x,y):
        if (x != 0) and (y != 0):
            return abs(x-y)/math.sqrt(abs(x*y))
        elif x != 0:
            return abs(x-y)/abs(x)
        elif y != 0:
            return abs(x-y)/abs(y)
        else:
            return 0

    sum = 0
    for key in summaryStats1.keys():
        v1 = summaryStats1[key]
        v2 = summaryStats2[key]
        if isinstance(v1, tuple):
            for i in range(3):
                sum += percentDiff(v1[i], v2[i])
        else:
            sum += percentDiff(v1,v2)

    return sum

modelName = 'Stochastic_SymTree' # 'Fern, Connifer etc'

# ------------------------------------------------------------------------------
# Control panel for main runs
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    s = model({'rule_1_0': 0, 'rule_1_1': 0})
    s2 =model({})

    d = distance(s,s2)
    # s = model({})

    print()
    print('---------------')
    print('Model summary')
    print('---------------')
    print()

    for (k,v) in s.items():
        print(k, ':', v)
        print()
