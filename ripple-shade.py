import rhinoscriptsyntax as rs
import math
from utils.easing import easeInOutSine
from utils.reset import reset
from utils.geom import box2pt

reset()

def shortest_angle_distance(angle1, angle2):
    diff = abs(angle1 - angle2)
    return min(diff, 2 * math.pi - diff)

radius_mm = 85
numPoints = 300
height = 356
slices = 200
amplitude = 1.5
wavelengthStart = 1.1 #2
wavelengthMultiplier = 0.008
# rocks = ([radius_mm, 0, 50], [0, radius_mm, 300], [0, -radius_mm, 225], [-radius_mm, 0, 125])
# rocks = ([radius_mm, 0, 50])
# z, angle, radius, waveOffset
rocks = ([50, math.pi * 0.2, 100, 0], 
         [220, math.pi * 0.5, 70, 0], 
         [125, math.pi * 0.9, 50, math.pi], 
         [300, math.pi * 1.2, 90, 0], 
         [100, math.pi * 1.6, 140, math.pi], 
         [270, math.pi * 1.85, 30, 0])

curves = []
curves2 = []
for s in range(slices):
    points = []
    points2 = []
    z = s * height / slices
    for i in range(numPoints + 1):   
        angle = 2 * math.pi * i / numPoints
        x = radius_mm * math.cos(angle)
        y = radius_mm * math.sin(angle)
        pointOnCylinder = (x, y, z)
        radOffset = 0.0
        for rock in rocks:
            
            # dist = rs.Distance(rock, pointOnCylinder) + 4
            distY = rock[0] - z
            distX = shortest_angle_distance(rock[1], angle) * radius_mm
            dist = math.sqrt(distX * distX + distY * distY)

            ripplePeak = rock[2]
            rippleAttack = ripplePeak * 0.3
            rippleDecay = ripplePeak * 2.5

            wavelength = wavelengthStart + dist * wavelengthMultiplier

            if (dist < rippleDecay and dist > rippleAttack):
                waveForm = math.sin(dist / wavelength + rock[3]) * amplitude
                if (dist < ripplePeak):
                    radOffset += easeInOutSine(dist - rippleAttack, 0, waveForm, ripplePeak - rippleAttack)
                else:
                    radOffset += easeInOutSine(rippleDecay - dist, 0, waveForm, rippleDecay - ripplePeak)
                    
        x2 = (radius_mm + radOffset) * math.cos(angle)
        y2 = (radius_mm + radOffset) * math.sin(angle)
        points.append([x2,y2,z])

        x2 = (radius_mm + radOffset - 0.5) * math.cos(angle)
        y2 = (radius_mm + radOffset - 0.5) * math.sin(angle)
        points2.append([x2,y2,z])

    curves.append(rs.AddInterpCurve(points))
    curves2.append(rs.AddInterpCurve(points2))

surf = rs.AddLoftSrf(curves)
surf2 = rs.AddLoftSrf(curves2)
rs.DeleteObjects(curves)
rs.DeleteObjects(curves2)

# cyl = rs.AddCylinder([0,0,0], height, radius_mm + 10)

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
