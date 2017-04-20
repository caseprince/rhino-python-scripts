import rhinoscriptsyntax as rs

def reset():
    arr1 = rs.AllObjects()
    if arr1: rs.DeleteObjects(arr1)
    rs.Command("ClearAllMeshes")
    rs.Command("ClearUndo")

reset()

radius = 80;
height = 350;
turns = 0.15;
twist = turns * 360;
fins = 33;

rail = rs.AddSpiral([0,0,0], [0,0,1], height/turns, turns, radius);
start = [radius, 15, 0];
end = [radius, -15, 0];
arc1 = rs.AddArc3Pt(start, end, [radius + 4, 0, 0]);
arc2 = rs.AddArc3Pt(start, end, [radius + 2, 0, 0]);
curve1 = rs.JoinCurves([arc1, arc2], True);
rs.RotateObject(curve1, [radius,0,0], 10);

vector = rs.VectorCreate([10,0,height/2], [0,0,0])
curve2 = rs.CopyObject(curve1, vector);
rs.RotateObject(curve2, [radius,0,0], 20);
rs.RotateObject(curve2, [0,0,0], twist/2);

vector = rs.VectorCreate([0,0,height], [0,0,0])
curve3 = rs.CopyObject(curve1, vector);
rs.RotateObject(curve3, [0,0,0], twist);

fin = rs.AddSweep1(rail, [curve1, curve2, curve3], True)
rs.CapPlanarHoles(fin);

vector = rs.VectorCreate([0,0,0], [0,0,0])
for i in range(fins):
    newFin = rs.CopyObject(fin, vector);
    rs.RotateObject(newFin, [0,0,0], i * (360/fins));
