import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math
from utils.easing import easeInSine
from utils.reset import reset

reset()

radius_mm = 108
numPoints = 300
height = 400
slices = 200
rippleDecay = 330
amplitude = 4
wavelength = 4
rocks = ([radius_mm, 0, 50], [0, radius_mm, 350], [0, -radius_mm, 250], [-radius_mm, 0, 150], )

curves = []
for s in range(slices):
    points = []
    z = s * height / slices
    for i in range(numPoints + 1):     
        x = radius_mm * math.cos(2 * math.pi * i / numPoints)
        y = radius_mm * math.sin(2 * math.pi * i / numPoints)
        pointOnCylinder = (x, y, z)
        radOffset = 0.0
        for rock in rocks:
            
            dist = rs.Distance(rock, pointOnCylinder) + 7
            if (dist < rippleDecay):
                radOffset += easeInSine(rippleDecay - dist, 0, math.sin(dist / wavelength) * amplitude, rippleDecay)

        x2 = (radius_mm + radOffset) * math.cos(2 * math.pi * i / numPoints)
        y2 = (radius_mm + radOffset) * math.sin(2 * math.pi * i / numPoints)
        points.append([x2,y2,z])

    curves.append(rs.AddInterpCurve(points))

rs.AddLoftSrf(curves)
rs.DeleteObjects(curves)

rs.ViewDisplayMode("Perspective", "Shaded")
rs.ViewDisplayMode("Perspective", "Rendered")
