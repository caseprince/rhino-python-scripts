import rhinoscriptsyntax as rs
import math, random
from utils.easing import *

phis = []

def fibonacci_sphere(samples=1, randomize=True, radius=2.5):
    rnd = 1.
    if randomize:
        rnd = random.random() * samples

    points = []
    offset = 2.0/samples
    increment = math.pi * (3.0 - math.sqrt(5.0))

    for i in range(samples - 2):
        # z = (((i * offset) - 1) + (offset / 2))
        z = easeInOutSine(i+1, -1, 2, samples)

        r = math.sqrt(1 - pow(z,2))

        phi = ((i+1 + rnd) % samples) * increment
        phis.append(phi % (math.pi*2))

        x = math.cos(phi) * r * radius
        y = math.sin(phi) * r * radius
        z *= -radius

        points.append([x,y,z])

    return points

def addPts(pt1, pt2):
    return [pt1[0]+pt2[0], pt1[1]+pt2[1], pt1[2]+pt2[2]]

def box2pt(p1, p2):

    pt0 = p1
    pt1 = rs.coerce3dpoint([p2[0], p1[1], p1[2]])
    pt2 = rs.coerce3dpoint([p2[0], p2[1], p1[2]])
    pt3 = rs.coerce3dpoint([p1[0], p2[1], p1[2]])
    pt4 = rs.coerce3dpoint([p1[0], p1[1], p2[2]])
    pt5 = rs.coerce3dpoint([p2[0], p1[1], p2[2]])
    pt6 = p2
    pt7 = rs.coerce3dpoint([p1[0], p2[1], p2[2]])

    return rs.AddBox([pt0, pt1, pt2, pt3, pt4, pt5, pt6, pt7])

def reset():
    arr1 = rs.AllObjects()
    if arr1: rs.DeleteObjects(arr1)
    rs.Command("ClearAllMeshes")
    rs.Command("ClearUndo")

# reset()

# 12" w/ larger petals
radius_mm = 100
sq_mm_per_petal = 160
s = 160

surfaceArea = 4 * math.pi * radius_mm**2
petals = 512 # int(surfaceArea / sq_mm_per_petal)
points = fibonacci_sphere(petals, False, radius_mm)

petal = rs.GetObject("Select Petal")
# petalInner = rs.GetObject("Select Petal Inner")

rMin = .35
rMax = .9
rDiff = rMax - rMin
i = 0

aMin = -45
aMax = -90

numPts = len(points)

boolean = rs.FirstObject()

for i in range(numPts): # numPts
# for pt in points:

    pt = points[i]

    vector = rs.VectorCreate(pt, [0,0,0])
    newPetal = rs.CopyObject(petal, vector)
    # newPetalInner = rs.CopyObject(petalInner, vector)

    angle = easeInSine(i, aMin, aMax - aMin, numPts)
    rs.RotateObjects([newPetal], pt, angle, [1,0,0], False)

    if i < numPts / 2:
        scale = easeOutSine(i, rMin, rDiff, numPts / 2)
    else:
        scale = easeInSine(i - (numPts / 2), rMax, -rDiff, numPts / 2)
    rs.ScaleObjects([newPetal], pt, [scale,scale,scale])

    maxTilt = .25

    tilt = math.sin(((pt[2]/radius_mm) * math.pi) + (phis[i])) * maxTilt
    # rs.OrientObject(newPetal, [pt, addPts(pt,[0,0,-1]), addPts(pt,[0,1,0])], [pt, [0,0,0], addPts(pt,[0,0,1])])
    rs.OrientObject(newPetal, [pt, addPts(pt,[tilt,0,-1]), addPts(pt,[0,1,0])], [pt, [0,0,0], addPts(pt,[0,0,1])])
    # rs.OrientObject(newPetalInner, [pt, addPts(pt,[tilt,0,-1]), addPts(pt,[0,1,0])], [pt, [0,0,0], addPts(pt,[0,0,1])])

    # if i == 0:
    #     boolean = newPetal
    #     rs.DeleteObject(newPetalInner)
    # else:
    #     boolean = rs.BooleanUnion([boolean, newPetal])
    #     boolean = rs.BooleanDifference([boolean], [newPetalInner])

    i = i + 1
