import math

# Initialize empty lists for vertices, normals, and faces.
radius = 1 
num_sides = 8  
width = 0.5 
vertices = []
normals = []
faces = []

# Calculate the central angle between sides.
central_angle = 360.0 / num_sides


for i in range(num_sides):
    # Calculate the angle in radians.
    angle = math.radians(i * central_angle)

    # Calculate the x and y coordinates of the vertex.
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    magnitude = math.sqrt(x * x + y * y+ 0*0)
    a= x/magnitude
    b= y/magnitude
    c= 0/magnitude
    # Append the vertices and normals to the respective lists.
    vertices.append((x, y, 0.0))
    normals.append((a, b, c))

# Write the data to an OBJ file.
with open('output.obj', 'w') as obj_file:
    obj_file.write("# OBJ file\n")
    obj_file.write(f"# Vertices: {len(vertices)}\n")
    for vertex in vertices:
        obj_file.write(f"v {' '.join(map(str, vertex))}\n")
    obj_file.write(f"# Normals: {len(normals)}\n")
    for normal in normals:
        obj_file.write(f"vn {' '.join(map(str, normal))}\n")

    obj_file.write(f"# Faces: {num_sides}\n")
    for i in range(num_sides):
        v1 = i + 1
        v2 = (i + 1) % num_sides + 1
        v3 = num_sides + 1  # Central vertex

        n = i + 1  # Normals

        obj_file.write(f"f {v1}//{n} {v2}//{n} {v3}//{n}\n")

