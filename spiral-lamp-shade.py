import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

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

#reset()

w = 140 # unit width
h = 13  # unit height
d = 7.857 # distance
t = .1  # unit thickness
ct = .6 # cap thickness
c = 42  # count
twist = 180

c1 = w/2;
c2 = c1 - t;
c3 = (w/2) - h;

box_neg = box2pt([-c2, -c2, 0], [c2, c2, h])
box_bottom_neg = box2pt([-c2, -c2, 0 + ct], [c2, c2, h + (ct*2)])
box_bottom_neg2 = box2pt([-c3, -c3, 0], [c3, c3, h])

box_top_neg = box2pt([-c2, -c2, 0 - ct], [c2, c2, h - ct])
box_top_neg2 = box2pt([-c3, -c3, 0], [c3, c3, h])

box = box2pt([-c1, -c1, 0], [c1, c1, h])
box_bottom = rs.BooleanDifference([box], [box_bottom_neg, box_bottom_neg2])[0]
box = box2pt([-c1, -c1, 0], [c1, c1, h])
box_middle = rs.BooleanDifference([box], [box_neg])[0]
box = box2pt([-c1, -c1, 0], [c1, c1, h])
box_top = rs.BooleanDifference([box], [box_top_neg, box_top_neg2])[0]

for i in range(c):
    vector = rs.VectorCreate([0,0,i*d], [0,0,0])
    if i == 0:
        b = rs.CopyObject(box_bottom, vector)
    elif i == c - 1:
        b = rs.CopyObject(box_top, vector)
    else:
        b = rs.CopyObject(box_middle, vector)

    rs.RotateObject(b, [0,0,0], (i/(c-1))*twist, rg.Vector3d.ZAxis)

rs.DeleteObjects([box_bottom, box_top, box_middle])
