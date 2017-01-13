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

# time, beginning, change, duration
def easeInOutCubic(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t + b
    t -= 2
    return c/2*(t*t*t + 2) + b

reset()

r = 6  # half-size
d = 9  # distance
w = 15 # width
h = 35 # height
c = (w - 1) * d / 2 # center offset
twist = 180

for x in range(w):
    for y in range(w):
        for z in range(h):

            if x == 0 or x + 1 == w or y == 0 or y + 1 == w:

                b = box2pt([r,r,r], [-r,-r,-r])

                if z < h / 2:
                    ratio = easeInOutCubic(z, 0, 1, h/2)
                else:
                    ratio = easeInOutCubic(z-(h/2), 1, -1, h/2)

                rs.RotateObject(b, [0,0,0], (x + z) * 2 * ratio, rg.Vector3d.XAxis)
                rs.RotateObject(b, [0,0,0], (y - z) * 2 * ratio, rg.Vector3d.YAxis)
                rs.RotateObject(b, [0,0,0], z * 2 * ratio, rg.Vector3d.ZAxis)

                rs.RotateObject(b, [0,0,0], z / (h-1) * 90, rg.Vector3d.XAxis)
                rs.RotateObject(b, [0,0,0], z / (h-1) * -90, rg.Vector3d.YAxis)

                pt = [x * d - c, y * d - c, z * d]
                rs.MoveObject(b, rs.VectorCreate(pt, [0,0,0]))
                rs.RotateObject(b, [0,0,0], z * (twist / (h-1)), rg.Vector3d.ZAxis)
