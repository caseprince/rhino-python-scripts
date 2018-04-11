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

# reset()

# pyramids
radius_mm = 32
petals = 120

# truncated pyramids
radius_mm = 140 # 130
petals = 189 # 188
angle = 38

# sm truncated pyramids
# radius_mm = 43
# petals = 23
# angle = 58


points = fibonacci_sphere(petals, False, radius_mm)

petal = rs.GetObjects("Pick some object")

for pt in points:

    vector = rs.VectorCreate(pt, [0,0,0])
    newPetal = rs.CopyObject(petal)

    # angle = math.atan2(pt[1], pt[2]) * 45 / math.pi
    # angle = angle + pt[2]
    rs.RotateObject(newPetal, [0,0,0], angle, rg.Vector3d.ZAxis)
    rs.MoveObject(newPetal, vector)

    rs.OrientObject(newPetal, [pt, addPts(pt,[0,0,-1]), addPts(pt,[0,1,0])], [pt, [0,0,0], addPts(pt,[0,0,1])])
