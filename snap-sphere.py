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

reset()



# 18cm diameter on connex
# r = 90 # radius
# t = 1.5 # thickness
# jh = 1 # half joint height
# jo = 0.05 # joint overlap
# gx = 0.05 # half gap xy
# tz = 0.0125 # top z gap
# gz = 0.1 # gap z
# bz = 0.0125 # bottom z gap


# 16cm J750 test
r = 80 # radius
t = 2 # thickness
jh = 1 # half joint height
jo = 0.15 # joint overlap
gx = 0.03 # half gap xy
tz = 0.0125 # top z gap
gz = 0.1 # gap z
bz = 0.0125 # bottom z gap


# 22cm diameter on connex
r = 110 # radius
t = 1.5 # thickness
jh = 1 # half joint height
jo = 0.25 # joint overlap
gx = 0.06 # half gap xy
tz = 0.0125 # top z gap
gz = 0.1 # gap z
bz = 0.0125 # bottom z gap

# 6cm diameter on connex
r = 30 # radius
t = 2 # thickness
jh = 1 # half joint height
jo = 0.2 # joint overlap
gx = 0.09 # half gap xy
tz = 0.0125 # top z gap
bz = 0.0125 # bottom z gap

# 15cm diameter on connex (matte)
r = 75 # radius
t = 1.5 # thickness
jh = 1 # half joint height
jo = 0.25 # joint overlap
gx = 0.08 # half gap xy
tz = 0.0125 # top z gap
gz = 0.05 # gap z
bz = 0.0125 # bottom z gap

# 6cm diameter on j750
r = 30 # radius
t = 1.5 # thickness
jh = 1 # half joint height
jo = 0.3 # joint overlap
gx = 0.05 # half gap xy
tz = 0.0125 # top z gap
bz = 0.0125 # bottom z gap

# 20cm diameter on connex
r = 100 # radius
t = 1.5 # thickness
jh = 1 # half joint height
jo = 0.15 # joint overlap
gx = 0.03 # half gap xy
tz = 0.0125 # top z gap
gz = 0.1 # gap z
bz = 0.0125 # bottom z gap

# 18cm diameter THIC on j750
r = 90 # radius
t = 10 # thickness
jh = 1 # half joint height
jo = 0 # 0.15 # joint overlap
gx = 0.09 # half gap xy
tz = 0.0125 # top z gap
gz = 0.1 # gap z
bz = 0.0125 # bottom z gap

r_inner = r -(t/2) -(jo/2)
r_outer = r -(t/2) +(jo/2)

r_inner = r -(t * 0.8) -(jo/2)
r_outer = r -(t * 0.8) +(jo/2)

# top half
top_half = rs.AddSphere([0, 0, 0], r)
diff_box = box2pt([r, r, -jh], [-r, -r, -r])
diff_sphere = rs.AddSphere([0, 0, 0], r - t)

joint_circle_top = rs.AddCircle([0, 0, 0], r_inner + gx)
joint_circle_bottom = rs.AddCircle([0, 0, -jh], r_outer + gx)
rail1 =  rs.AddLine([r_inner, 0, 0], [r_outer, 0, -jh])
rail2 =  rs.AddLine([0, r_inner, 0], [0, r_outer, -jh])
diff_inner_lower = rs.AddSweep2([rail1, rail2], [joint_circle_top, joint_circle_bottom], True)
rs.CapPlanarHoles(diff_inner_lower)
rs.DeleteObjects([rail1, rail2])
diff_inner_upper = rs.CopyObject(diff_inner_lower, [0, 0, jh])
silly_cylinder = rs.AddCylinder([0,0,0 -jh], bz, r)
top_half = rs.BooleanDifference([top_half], [diff_box, diff_sphere, diff_inner_lower, diff_inner_upper, silly_cylinder])[0]

# bottom half
bottom_half = rs.AddSphere([0, 0, 0], r)
diff_box = box2pt([r, r, jh], [-r, -r, r])
diff_sphere = rs.AddSphere([0, 0, 0], r - t)
bottom_half = rs.BooleanDifference([bottom_half], [diff_box, diff_sphere])[0]

joint_circle_top = rs.AddCircle([0, 0, 0], r_inner - gx)
joint_circle_bottom = rs.AddCircle([0, 0, -jh -(0)], r_outer - gx)
rail1 =  rs.AddLine([r_inner, 0, -0], [r_outer, 0, -jh -(0)])
rail2 =  rs.AddLine([0, r_inner, -0], [0, r_outer, -jh -(0)])
diff_inner_lower = rs.AddSweep2([rail1, rail2], [joint_circle_top, joint_circle_bottom], True)
rs.CapPlanarHoles(diff_inner_lower)
rs.DeleteObjects([rail1, rail2])
diff_inner_upper = rs.CopyObject(diff_inner_lower, [0, 0, jh])

silly_cylinder = rs.AddCylinder([0,0,-jh - 0], (jh*2) + 0, r)
outer_diff = rs.BooleanDifference([silly_cylinder], [diff_inner_lower, diff_inner_upper])[0]
silly_cylinder = rs.AddCylinder([0,0,jh - tz], tz, r)
bottom_half = rs.BooleanDifference([bottom_half], [outer_diff, silly_cylinder])[0]
