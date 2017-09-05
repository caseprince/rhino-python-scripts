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
    #rs.Command("ClearAllMeshes")
    rs.Command("ClearUndo")

reset()

w = 333;
h = 254;
d = 10;

rows = 6;
cols = 5;

frame = box2pt([0, 0, 0], [w, h-1, d])

holeW = 51;
holeH = 38;

paddingW = 20;
paddingH = 5;
holesWidth = w - (paddingW * 2) - holeW
holesHeight = h - (paddingH * 2) - holeH

bevel = 1;
plane = rs.WorldXYPlane()

for x in range(0, cols):
    for y in range(0, rows):
        holeX = paddingW + (holesWidth * (x/(cols-1)))
        holeY = paddingH + (holesHeight * (y/(rows-1)))

        hole1 = box2pt([holeX, holeY+1, d-2], [holeX + holeW, holeY + holeH - 1, d])
        hole2 = box2pt([holeX, holeY, d-2], [holeX + holeW, holeY + holeH, d-1])

        hole3 = box2pt([holeX, holeY, 0], [holeX + holeW, holeY + holeH, d-4])

        rect_top = rs.AddRectangle( plane, holeW + 2, holeH )
        rs.MoveObject(rect_top, [holeX - bevel, holeY, d])

        rect_bottom = rs.AddRectangle( plane, holeW, holeH - 2)
        rs.MoveObject(rect_bottom, [holeX, holeY+1, d-1])

        rail =  rs.AddLine([holeX+(holeW/2), holeY+(holeH/2),d-1], [holeX+(holeW/2), holeY+(holeH/2),d])

        top_sup_neg = rs.AddSweep1(rail, [rect_bottom, rect_top], True)
        rs.CapPlanarHoles(top_sup_neg)

        frame = rs.BooleanDifference([frame], [hole1, hole2, top_sup_neg, hole3])[0]
