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
                face = [list(map(int, vertex.split('//'))) for vertex in face]
                face = [face[i][0]-1 for i in range(len(face))]+[face[i][1]-1 for i in range(len(face))]
                faces.append(face)
            elif line.startswith('vn '):
                normal = list(map(float, line.split()[1:]))
                normals.append(normal)

    return vertices, normals, faces

def dump_to_file(vertices, normals, faces, output_file):
    with open(output_file, 'w') as file:
        """file.write("vertices = []\n")
        read = 0
        while read <= len(vertices):
            file.write("vertices += " + str(vertices[read:][:blockSize]) + "\n")
            read += blockSize

        file.write("normals = []\n")
        read = 0
        while read <= len(normals):
            file.write("normals += " + str(normals[read:][:blockSize]) + "\n")
            read += blockSize

        file.write("faces = []\n")
        read = 0
        while read <= len(faces):
            file.write("faces += " + str(faces[read:][:blockSize]) + "\n")
            read += blockSize"""
        file.write("vertices = " + str(vertices) + "\n")
        file.write("normals = " + str(normals) + "\n")
        file.write("faces = " + str(faces) + "\n")
        file.write("\n")







obj_file_path = input('model to use: ')
loaded_vertices, loaded_normals, loaded_faces = load_obj(obj_file_path)

output_file_path = input('file to output to: ')
dump_to_file(loaded_vertices, loaded_normals, loaded_faces, output_file_path)
