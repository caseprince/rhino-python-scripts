import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math, random


# time, beginning, change, duration
def easeInOutCubic(t, b, c, d):
    t /= d/2
    if t < 1:
        return c/2*t*t*t + b
    t -= 2
    return c/2*(t*t*t + 2) + b

def easeOutSine(t, b, c, d):
	return c * math.sin(t/d * (math.pi/2)) + b
def easeInSine(t, b, c, d):
	return -c * math.cos(t/d * (math.pi/2)) + c + b

def easeInOutCirc(t, b, c, d):
	t /= d/2
	if t < 1:
		return -c/2 * (math.sqrt(1 - t*t) - 1) + b
	t -= 2
	return c/2 * (math.sqrt(1 - t*t) + 1) + b

def reset():
    arr1 = rs.AllObjects()
    if arr1: rs.DeleteObjects(arr1)
    rs.Command("ClearAllMeshes")
    rs.Command("ClearUndo")

reset()


radius_mm = 108
numPoints = 300
height = 400
slices = 200
rippleDecay = 330
amplitude = 4
wavelength = 4

print("hello")

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
