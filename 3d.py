from gturtle import *
from math import *


makeTurtle()


def draw_triangle(pos):
    setPos(pos[0])
    startPath()
    moveTo(pos[1])
    moveTo(pos[2])
    #moveTo(pos[0]) #
    fillPath()

def matrix_multiply(a, b):
    result = []

    if isinstance(a[0], (int, float)):
        a = [a]

    if isinstance(b[0], (int, float)):
        b = [b]

    for i in range(len(a)):
        row_result = []
        for j in range(len(b[0])):
            element_sum = sum(a[i][k] * b[k][j] for k in range(len(b)))
            row_result.append(element_sum)
        result.append(row_result)

    if len(result) == 1:
        return result[0]

    return result

def matrix_vector_multiply(matrix, vector):
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]
    
    
def add(vec1, vec2):
    return [x + y for x, y in zip(vec1, vec2)]

def sub(vec1, vec2):
    return [x - y for x, y in zip(vec1, vec2)]
    
def mul(vec, scalar):
    return [x * scalar for x in vec]
    
def div(vec, scalar):
    return [x / scalar for x in vec]
    
def dot_product(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))

def cross_product(v1, v2):
    return [v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[0] * v2[1] - v1[1] * v2[0]]
    
def normalize(vector):
    length = sqrt(sum(x * x for x in vector))
    return [x / length for x in vector] if length != 0 else vector



def perspective_matrix(aspect_ratio, fov_y, near, far, screen_size):
    tan_half_fov_y = tan(fov_y / 2)
    range_inv = 1 / (far - near)

    return [
        [screen_size / (aspect_ratio * tan_half_fov_y), 0, 0, 0],
        [0, screen_size / tan_half_fov_y, 0, 0],
        [0, 0, -(far + near) * range_inv, -2 * far * near * range_inv],
        [0, 0, -1, 0]
    ]

def translation_matrix(translation_vector):
    return [
        [1, 0, 0, translation_vector[0]],
        [0, 1, 0, translation_vector[1]],
        [0, 0, 1, translation_vector[2]],
        [0, 0, 0, 1]
    ]

def scale_matrix(scale_vector):
    return [
        [scale_vector[0], 0, 0, 0],
        [0, scale_vector[1], 0, 0],
        [0, 0, scale_vector[2], 0],
        [0, 0, 0, 1]
    ]

def rotation_matrix_x(theta):
    return [
        [1, 0, 0, 0],
        [0, cos(theta), -sin(theta), 0],
        [0, sin(theta), cos(theta), 0],
        [0, 0, 0, 1]
    ]

def rotation_matrix_y(theta):
    return [
        [cos(theta), 0, sin(theta), 0],
        [0, 1, 0, 0],
        [-sin(theta), 0, cos(theta), 0],
        [0, 0, 0, 1]
    ]

def rotation_matrix_z(theta):
    return [
        [cos(theta), -sin(theta), 0, 0],
        [sin(theta), cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
def is_visible(pos):
    return (pos[2][1] - pos[0][1]) * (pos[1][0] - pos[0][0]) > (pos[1][1] - pos[0][1]) * (pos[2][0] - pos[0][0])

def poly_sort(poly):
    return -(tranf_verts[poly[0]][2] + tranf_verts[poly[1]][2] + tranf_verts[poly[2]][2])

projection_matrix = perspective_matrix(1, radians(110), 0.01, 100, 700)

vertices = [[0.0, -1.0, -1.0], [0.464723, -1.0, -0.885456], [0.822984, -1.0, -0.568065], [0.992709, -1.0, -0.120537], [0.935016, -1.0, 0.354605], [0.663123, -1.0, 0.748511], [0.239316, -1.0, 0.970942], [-0.239316, -1.0, 0.970942], [-0.663123, -1.0, 0.748511], [-0.935016, -1.0, 0.354605], [-0.992709, -1.0, -0.120537], [-0.822984, -1.0, -0.568065], [-0.464723, -1.0, -0.885456], [0.0, 1.0, 0.0]]
normals = [[0.2153, 0.4367, -0.8735], [0.5965, 0.4367, -0.6734], [0.8411, 0.4367, -0.319], [0.893, 0.4367, 0.1084], [0.7404, 0.4367, 0.511], [0.4181, 0.4367, 0.7966], [-0.0, 0.4367, 0.8996], [-0.4181, 0.4367, 0.7966], [-0.7404, 0.4367, 0.511], [-0.893, 0.4367, 0.1084], [-0.8411, 0.4367, -0.319], [-0.0, -1.0, -0.0], [-0.5965, 0.4367, -0.6734], [-0.2153, 0.4367, -0.8735]]
faces = [[0, 13, 1, 0, 0, 0], [1, 13, 2, 1, 1, 1], [2, 13, 3, 2, 2, 2], [3, 13, 4, 3, 3, 3], [4, 13, 5, 4, 4, 4], [5, 13, 6, 5, 5, 5], [6, 13, 7, 6, 6, 6], [7, 13, 8, 7, 7, 7], [8, 13, 9, 8, 8, 8], [9, 13, 10, 9, 9, 9], [10, 13, 11, 10, 10, 10], [1, 5, 9, 11, 11, 11], [11, 13, 12, 12, 12, 12], [12, 13, 0, 13, 13, 13], [12, 0, 1, 11, 11, 11], [1, 2, 3, 11, 11, 11], [3, 4, 5, 11, 11, 11], [5, 6, 7, 11, 11, 11], [7, 8, 9, 11, 11, 11], [9, 10, 11, 11, 11, 11], [11, 12, 1, 11, 11, 11], [1, 3, 5, 11, 11, 11], [5, 7, 9, 11, 11, 11], [9, 11, 1, 11, 11, 11]]
 


playground = getPlayground()
playground.enableRepaint(False)
setPenColor("Black")

t = 0
while True:
    tranf_mat = matrix_multiply(projection_matrix, translation_matrix([0, 0, -3]))
    tranf_mat = matrix_multiply(tranf_mat, rotation_matrix_x(sin(t*2)/2))
    tranf_mat = matrix_multiply(tranf_mat, rotation_matrix_y(t))

    tranf_verts = []
    for vertex in vertices:
        vert = matrix_vector_multiply(tranf_mat, vertex + [1])
        tranf_verts.append([vert[v] / vert[3] for v in range(0, 3)])
    
    

    playground.clear()
    for face in sorted(faces, key=poly_sort):
        pos = [tranf_verts[face[tri]] for tri in range(0, 3)]
        
        if is_visible(pos):
            color = [n*0.5+0.5 for n in normals[face[3]]]
    
            
            setPenColor(color)
            setFillColor(color)
            draw_triangle(pos)

    
    playground.repaint()
    t += 0.001