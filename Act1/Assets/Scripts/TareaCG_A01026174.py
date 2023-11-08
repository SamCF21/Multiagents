#Samantha Covarrubias
#A01026174
#Tarea 1
import math

radius = 1
width = 0.5
sides = 8
vertices = []
faces = []
normals = []

#Calculate the angle of the triangle
angle = 360 / sides

for i in range(sides):
#Calculate the angle in radians
    angleRad = math.radians(i * angle)

    #Calculate the height of the triangle
    x = radius * math.cos(angleRad)

    #Calculate the width of the triangle
    y= radius * math.sin(angleRad)

    #Calculate vertices
    vertices.append((x,y,0))

    magnitude = math.sqrt(x * x + y * y+ 0*0)
    a= x/magnitude
    b= y/magnitude
    c= 0/magnitude

    #Calculate normals
    normals.append((a,b,c))



with open("output.obj", "w") as obj_file:
    obj_file.write("# OBJ File\n")

    obj_file.write("# Vertices: " + str(len(vertices)) + "\n")
    for vertex in vertices:
        obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
    obj_file.write("# Normals: " + str(len(normals)) + "\n")
    for normal in normals:
        obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
    obj_file.write(f"# Faces: {sides}\n")
    for i in range(sides):
        v1 = i + 1
        v2 = (i + 1) % sides + 1
        v3 = sides + 1  # Central vertex

        n = i + 1  # Normals
        obj_file.write(f"f {v1}//{n} {v2}//{n} {v3}//{n}\n")