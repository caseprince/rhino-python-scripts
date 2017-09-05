import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math, random

def fibonacci_sphere(samples=1, randomize=True, radius=2.5):
    rnd = 1.
    if randomize:
        rnd = random.random() * samples

    points = []
    offset = 2./samples
    increment = math.pi * (3. - math.sqrt(5.));

    for i in range(samples):
        z = (((i * offset) - 1) + (offset / 2));
        r = math.sqrt(1 - pow(z,2))

        phi = ((i + rnd) % samples) * increment

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

reset()

# 10"
# radius_mm = 127
# petals = 4098

# 8.5"
radius_mm = 108
sq_mm_per_petal = 50.25 # 50.25 square mm per petal
s = 35 #30.48 #0.48 * radius_mm

# 12" w/ larger petals
radius_mm = 152
sq_mm_per_petal = 160
s = 60

surfaceArea = 4 * math.pi * radius_mm**2
petals = int(surfaceArea / sq_mm_per_petal)
points = fibonacci_sphere(petals, False, radius_mm)


cone = rs.AddCone([0,0,0], .2 * s, .2 * s, True)
cone2 = rs.AddCone([0,-.05 * s,0], .21 * s, .19 * s, True)
petal = rs.BooleanDifference([cone], [cone2])[0]
rs.RotateObject(petal, [0,0,0], -13, rg.Vector3d.XAxis)

clipBoxZ = .43 * s
clipBox = box2pt([.3 * s, .3 * s, (.3 * s) + clipBoxZ], [-.3 * s, -.3 * s, (-.3 * s) + clipBoxZ])
rs.RotateObject(clipBox, [0,0,0], 5, rg.Vector3d.XAxis)
petal = rs.BooleanDifference([petal], [clipBox])[0]


for pt in points:
# while i < len(points):
    # pt = points[i]
    vector = rs.VectorCreate(pt, [0,0,0])
    newPetal = rs.CopyObject(petal, vector)

    rs.OrientObject(newPetal, [pt, addPts(pt,[0,0,1]), addPts(pt,[0,1,0])], [pt, [0,0,0], addPts(pt,[0,0,1])])

    #i += 1
