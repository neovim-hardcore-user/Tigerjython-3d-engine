def load_obj(file_path):
    vertices = []
    normals = []
    faces = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face = line.split()[1:]
                face = [list(map(int, vertex.split('/'))) for vertex in face]
                face = [face[i][0]-1 for i in range(len(face))]
                faces.append(face)

    return vertices, normals, faces

def dump_to_file(vertices, normals, faces, output_file):
    with open(output_file, 'w') as file:
        file.write("vertices = " + str(vertices) + "\n")

        file.write("faces = " + str(faces) + "\n" + " ")



obj_file_path = 'monkey.obj'
loaded_vertices, loaded_normals, loaded_faces = load_obj(obj_file_path)

output_file_path = 'output.py'
dump_to_file(loaded_vertices, loaded_normals, loaded_faces, output_file_path)
