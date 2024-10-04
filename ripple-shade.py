import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
from utils.easing import easeInSine
from utils.reset import reset
from utils.geom import box2pt

reset()

radius_mm = 80
numPoints = 300
height = 356
slices = 200
rippleDecay = 330
amplitude = 3
wavelength = 3
rocks = ([radius_mm, 0, 50], [0, radius_mm, 300], [0, -radius_mm, 225], [-radius_mm, 0, 125], )

curves = []
curves2 = []
for s in range(slices):
    points = []
    points2 = []
    z = s * height / slices
    for i in range(numPoints + 1):     
        x = radius_mm * math.cos(2 * math.pi * i / numPoints)
        y = radius_mm * math.sin(2 * math.pi * i / numPoints)
        pointOnCylinder = (x, y, z)
        radOffset = 0.0
        for rock in rocks:
            
            dist = rs.Distance(rock, pointOnCylinder) + 4
            if (dist < rippleDecay):
                radOffset += easeInSine(rippleDecay - dist, 0, math.sin(dist / wavelength) * amplitude, rippleDecay)

        x2 = (radius_mm + radOffset) * math.cos(2 * math.pi * i / numPoints)
        y2 = (radius_mm + radOffset) * math.sin(2 * math.pi * i / numPoints)
        points.append([x2,y2,z])

        x2 = (radius_mm + radOffset - 0.5) * math.cos(2 * math.pi * i / numPoints)
        y2 = (radius_mm + radOffset - 0.5) * math.sin(2 * math.pi * i / numPoints)
        points2.append([x2,y2,z])

    curves.append(rs.AddInterpCurve(points))
    curves2.append(rs.AddInterpCurve(points2))

surf = rs.AddLoftSrf(curves)
surf2 = rs.AddLoftSrf(curves2)
rs.DeleteObjects(curves)
rs.DeleteObjects(curves2)

cyl = rs.AddCylinder([0,0,0], height, radius_mm + 10)
# parts = rs.BooleanSplit(cyl, (surf, surf2))
# rs.DeleteObjects(parts[0], parts[2])

# rs.OffsetSurface(surf, 1, -0.1, False, True)
# rs.DeleteObjects(surf)

collarOffset = 60
collar = rs.AddCylinder([0,0,collarOffset], 8, 28)
hole = rs.AddCylinder([0,0,collarOffset], 8, 20.5)
collar = rs.BooleanDifference(collar, hole)

numSpokes = 12
spokeThickness = 2.2
spokeRadius = radius_mm + 10
spokes = []
for i in range(numSpokes):
    spoke = box2pt([spokeThickness / -2, 27, collarOffset], [spokeThickness / 2, spokeRadius, collarOffset + 8])
    rs.CurrentView("Right") # This can oddly affect the ShearObject function
    rs.ShearObject(spoke, [0,27,0], [0, spokeRadius, 0], -45)
    rs.RotateObject(spoke, [0,0,collarOffset], i * 360 / numSpokes, [0,0,1])
    spokes.append(spoke)

spokes.append(collar)
rs.BooleanUnion(spokes)

rs.ViewDisplayMode("Perspective", "Shaded")
rs.ViewDisplayMode("Perspective", "Rendered")
