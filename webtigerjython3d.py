from gturtle import *
from math import *


makeTurtle()

screen_size = 4000

def draw_triangle(pos):
    setPos(pos[0])
    startPath()
    moveTo(pos[1])
    moveTo(pos[2])
    #moveTo(pos[0]) #
    fillPath()

def matrix_multiply(matrix, vector):
    result = [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]
    return result
    
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

def perspective_matrix(aspect_ratio, fov_y, near, far):
    tan_half_fov_y = tan(fov_y / 2)
    range_inv = 1 / (far - near)

    return [
        [1 / (aspect_ratio * tan_half_fov_y), 0, 0, 0],
        [0, 1 / tan_half_fov_y, 0, 0],
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




def project_vertices(vertices, projection_matrix):
    projected_vertices = []
    for vertex in vertices:
        projected_vertex = matrix_multiply(projection_matrix, vertex + [1])
        scale = (1 / projected_vertex[3]) * screen_size
        projected_vertices.append([projected_vertex[0]*scale, projected_vertex[1]*scale, projected_vertex[2]])
    return projected_vertices

def translate(vertices, translation_vector):
    translation_matrix_ = translation_matrix(translation_vector)
    translated_vertices = [matrix_multiply(translation_matrix_, vertex + [1])[:3] for vertex in vertices]
    return translated_vertices

def scale(vertices, scale_vector):
    scale_matrix_ = scale_matrix(scale_vector)
    scaled_vertices = [matrix_multiply(scale_matrix_, vertex + [1])[:3] for vertex in vertices]
    return scaled_vertices
    
def rotate_x(vertices, theta):
    rotation_matrix_x = [
        [1, 0, 0, 0],
        [0, cos(theta), -sin(theta), 0],
        [0, sin(theta), cos(theta), 0],
        [0, 0, 0, 1]
    ]
    return [matrix_multiply(rotation_matrix_x, vertex + [1])[:3] for vertex in vertices]

def rotate_y(vertices, theta):
    rotation_matrix_y = [
        [cos(theta), 0, sin(theta), 0],
        [0, 1, 0, 0],
        [-sin(theta), 0, cos(theta), 0],
        [0, 0, 0, 1]
    ]
    return [matrix_multiply(rotation_matrix_y, vertex + [1])[:3] for vertex in vertices]

def rotate_z(vertices, theta):
    rotation_matrix_z = [
        [cos(theta), -sin(theta), 0, 0],
        [sin(theta), cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    return [matrix_multiply(rotation_matrix_z, vertex + [1])[:3] for vertex in vertices]

def rotate(vertices, angles):
    rx, ry, rz = angles
    rotated_vertices = rotate_x(vertices, rx)
    rotated_vertices = rotate_y(rotated_vertices, ry)
    rotated_vertices = rotate_z(rotated_vertices, rz)
    return rotated_vertices
    
def compute_normal(pos):
    vector1 = sub(pos[0], pos[1])
    vector2 = sub(pos[2], pos[1])
    
    normal = cross_product(vector1, vector2)
    
    
    return normalize(normal)

def poly_sort(poly):
    return -(pv[poly[0]][2] + pv[poly[1]][2] + pv[poly[2]][2])
    
    
    
def render_triangles():
    for i in sorted(faces, key=poly_sort):
        pos = [pv[i[0]], pv[i[1]], pv[i[2]]]
        avpos = div(add(add(tv[i[0]], tv[i[1]]), tv[i[2]]), 3)
        dif = max(dot_product(compute_normal([tv[i[0]], tv[i[1]], tv[i[2]]]), normalize(avpos)), 0.0)
        
        if dif > 0:
            dif = dif * 150 + 50
            color = (dif, 0, 0)
            setFillColor(color)
            setPenColor(color)
            draw_triangle(pos)

projection_matrix = perspective_matrix(1, radians(150), 0.1, 100)


vertices = [[-1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [0.0, 1.151714, 0.0], [0.7236, 1.704499, 0.52572], [-0.276385, 1.704499, 0.85064], [-0.894425, 1.704499, 0.0], [-0.276385, 1.704499, -0.85064], [0.7236, 1.704499, -0.52572], [0.276385, 2.598929, 0.85064], [-0.7236, 2.598929, 0.52572], [-0.7236, 2.598929, -0.52572], [0.276385, 2.598929, -0.85064], [0.894425, 2.598929, 0.0], [0.0, 3.151714, 0.0], [2.475873, -0.686786, -1.203428], [3.620401, -0.686786, -0.37188], [3.18323, -0.686786, 0.973594], [1.768516, -0.686786, 0.973594], [1.331345, -0.686786, -0.37188], [2.475873, 0.686786, 0.0], [-2.777166, -0.91434, -0.76346], [-2.777166, 0.91434, -0.76346], [-2.395437, -0.91434, -0.661176], [-2.395437, 0.91434, -0.661176], [-2.115991, -0.91434, -0.38173], [-2.115991, 0.91434, -0.38173], [-2.013707, -0.91434, 0.0], [-2.013707, 0.91434, 0.0], [-2.115991, -0.91434, 0.38173], [-2.115991, 0.91434, 0.38173], [-2.395437, -0.91434, 0.661176], [-2.395437, 0.91434, 0.661176], [-2.777166, -0.91434, 0.76346], [-2.777166, 0.91434, 0.76346], [-3.158896, -0.91434, 0.661176], [-3.158896, 0.91434, 0.661176], [-3.438342, -0.91434, 0.38173], [-3.438342, 0.91434, 0.38173], [-3.540626, -0.91434, 0.0], [-3.540626, 0.91434, 0.0], [-3.438342, -0.91434, -0.38173], [-3.438342, 0.91434, -0.38173], [-3.158896, -0.91434, -0.661176], [-3.158896, 0.91434, -0.661176], [-1.497772, -0.224641, -1.951997], [-1.189034, -0.269561, -1.924378], [-1.023236, -0.06809, -1.924378], [-1.543196, -0.06809, -1.924378], [-1.222335, 0.338335, -1.924378], [-0.876791, -0.036827, -1.924378], [-1.101194, -0.384261, -1.924378], [-1.523799, -0.333607, -1.951997], [-1.075131, 0.028991, -1.924378], [-1.223089, 0.194838, -1.924378], [-1.358299, 0.028991, -1.924378], [-0.735283, 0.287326, -1.924378], [-0.521375, 0.338335, -1.924378], [-0.156087, -0.059863, -1.924378], [-0.531248, -0.430088, -1.924378], [-0.751738, -0.387306, -1.924378], [-0.751738, -0.242507, -1.924378], [-0.55593, -0.29187, -1.924378], [-0.305822, -0.046699, -1.924378], [-0.531248, 0.203408, -1.924378], [-0.735283, 0.131009, -1.924378], [0.01833, 0.323526, -1.924378], [0.164775, 0.323526, -1.924378], [0.164775, -0.415279, -1.924378], [0.01833, -0.415279, -1.924378], [0.003521, 0.547306, -1.924378], [0.09073, 0.634515, -1.924378], [0.177938, 0.547306, -1.924378], [0.09073, 0.460098, -1.924378], [0.395137, 0.706915, -1.924378], [0.546518, 0.706915, -1.924378], [0.546518, -0.16188, -1.924378], [1.306714, 0.706915, -1.924378], [1.435058, 0.706915, -1.924378], [1.435058, -0.415279, -1.924378], [1.283677, -0.415279, -1.924378], [1.283677, 0.44858, -1.924378], [0.533355, -0.415279, -1.924378], [0.395137, -0.415279, -1.924378], [-1.497772, -0.224641, -2.161933], [-1.189034, -0.269561, -2.189552], [-1.023236, -0.06809, -2.189552], [-1.543196, -0.06809, -2.189552], [-1.222335, 0.338335, -2.189552], [-0.876791, -0.036827, -2.189552], [-1.101194, -0.384261, -2.189552], [-1.523799, -0.333607, -2.161933], [-1.075131, 0.028991, -2.189552], [-1.223089, 0.194838, -2.189552], [-1.358299, 0.028991, -2.189552], [-0.735283, 0.287326, -2.189552], [-0.521375, 0.338335, -2.189552], [-0.156087, -0.059863, -2.189552], [-0.531248, -0.430088, -2.189552], [-0.751738, -0.387306, -2.189552], [-0.751738, -0.242507, -2.189552], [-0.55593, -0.29187, -2.189552], [-0.305822, -0.046699, -2.189552], [-0.531248, 0.203408, -2.189552], [-0.735283, 0.131009, -2.189552], [0.01833, 0.323526, -2.189552], [0.164775, 0.323526, -2.189552], [0.164775, -0.415279, -2.189552], [0.01833, -0.415279, -2.189552], [0.003521, 0.547306, -2.189552], [0.09073, 0.634515, -2.189552], [0.177938, 0.547306, -2.189552], [0.09073, 0.460098, -2.189552], [0.395137, 0.706915, -2.189552], [0.546518, 0.706915, -2.189552], [0.546518, -0.16188, -2.189552], [1.306713, 0.706915, -2.189552], [1.435058, 0.706915, -2.189552], [1.435058, -0.415279, -2.189552], [1.283677, -0.415279, -2.189552], [1.283677, 0.44858, -2.189552], [0.533355, -0.415279, -2.189552], [0.395137, -0.415279, -2.189552], [1.44, 0.0, 2.71], [1.22, 0.381051, 2.71], [0.78, 0.381051, 2.71], [0.56, 0.0, 2.71], [0.78, -0.381051, 2.71], [1.22, -0.381051, 2.71], [0.897825, 0.0, 1.584163], [0.760657, 0.381051, 1.756166], [0.486322, 0.381051, 2.100171], [0.349154, 0.0, 2.272174], [0.486322, -0.381051, 2.100172], [0.760657, -0.381051, 1.756166], [-0.32043, 0.0, 1.306104], [-0.271476, 0.381051, 1.520588], [-0.173566, 0.381051, 1.949556], [-0.124612, 0.0, 2.16404], [-0.173566, -0.381051, 1.949556], [-0.271476, -0.381051, 1.520588], [-1.297395, 0.0, 2.085207], [-1.099182, 0.381051, 2.180662], [-0.702756, 0.381051, 2.371571], [-0.504543, 0.0, 2.467025], [-0.702756, -0.381051, 2.371571], [-1.099182, -0.381051, 2.180662], [-1.297395, 0.0, 3.334792], [-1.099182, 0.381051, 3.239338], [-0.702756, 0.381051, 3.048429], [-0.504543, 0.0, 2.952975], [-0.702756, -0.381051, 3.048429], [-1.099182, -0.381051, 3.239338], [-0.32043, 0.0, 4.113896], [-0.271476, 0.381051, 3.899412], [-0.173566, 0.381051, 3.470444], [-0.124612, 0.0, 3.25596], [-0.173566, -0.381051, 3.470444], [-0.271476, -0.381051, 3.899412], [0.897825, 0.0, 3.835838], [0.760657, 0.381051, 3.663835], [0.486322, 0.381051, 3.319829], [0.349154, 0.0, 3.147826], [0.486322, -0.381051, 3.319829], [0.760657, -0.381051, 3.663835]]
faces = [[1, 2, 0], [3, 6, 2], [7, 4, 6], [5, 0, 4], [6, 0, 2], [3, 5, 7], [1, 3, 2], [3, 7, 6], [7, 5, 4], [5, 1, 0], [6, 4, 0], [3, 1, 5], [8, 9, 10], [9, 8, 13], [8, 10, 11], [8, 11, 12], [8, 12, 13], [9, 13, 18], [10, 9, 14], [11, 10, 15], [12, 11, 16], [13, 12, 17], [9, 18, 14], [10, 14, 15], [11, 15, 16], [12, 16, 17], [13, 17, 18], [14, 18, 19], [15, 14, 19], [16, 15, 19], [17, 16, 19], [18, 17, 19], [20, 25, 21], [21, 25, 22], [22, 25, 23], [21, 23, 24], [23, 25, 24], [24, 25, 20], [24, 20, 21], [21, 22, 23], [27, 28, 26], [29, 30, 28], [31, 32, 30], [33, 34, 32], [35, 36, 34], [37, 38, 36], [39, 40, 38], [41, 42, 40], [43, 44, 42], [45, 46, 44], [47, 39, 31], [47, 48, 46], [49, 26, 48], [32, 40, 48], [27, 29, 28], [29, 31, 30], [31, 33, 32], [33, 35, 34], [35, 37, 36], [37, 39, 38], [39, 41, 40], [41, 43, 42], [43, 45, 44], [45, 47, 46], [31, 29, 27], [27, 49, 47], [47, 45, 43], [43, 41, 39], [39, 37, 35], [35, 33, 31], [31, 27, 47], [47, 43, 39], [39, 35, 31], [47, 49, 48], [49, 27, 26], [48, 26, 28], [28, 30, 32], [32, 34, 36], [36, 38, 40], [40, 42, 44], [44, 46, 48], [48, 28, 32], [32, 36, 40], [40, 44, 48], [55, 54, 59], [59, 54, 53], [55, 59, 58], [60, 59, 53], [55, 58, 60], [55, 60, 53], [56, 55, 52], [52, 55, 53], [56, 52, 51], [51, 50, 57], [56, 51, 57], [63, 62, 69], [69, 62, 61], [69, 61, 70], [63, 69, 68], [63, 68, 67], [64, 63, 67], [67, 66, 65], [64, 67, 65], [77, 76, 75], [78, 77, 75], [73, 72, 71], [73, 71, 74], [84, 83, 82], [84, 82, 86], [86, 82, 81], [81, 80, 79], [81, 79, 88], [84, 86, 85], [87, 86, 81], [87, 81, 88], [94, 98, 93], [98, 92, 93], [94, 97, 98], [99, 92, 98], [94, 99, 97], [94, 92, 99], [95, 91, 94], [91, 92, 94], [95, 90, 91], [90, 96, 89], [95, 96, 90], [102, 108, 101], [108, 100, 101], [108, 109, 100], [102, 107, 108], [102, 106, 107], [103, 106, 102], [106, 104, 105], [103, 104, 106], [116, 114, 115], [117, 114, 116], [112, 110, 111], [112, 113, 110], [123, 121, 122], [123, 125, 121], [125, 120, 121], [120, 118, 119], [120, 127, 118], [123, 124, 125], [126, 120, 125], [126, 127, 120], [67, 105, 66], [74, 112, 73], [68, 106, 67], [76, 114, 75], [60, 98, 59], [77, 115, 76], [83, 121, 82], [62, 100, 61], [88, 126, 87], [78, 116, 77], [79, 127, 88], [63, 101, 62], [69, 107, 68], [80, 118, 79], [64, 102, 63], [81, 119, 80], [65, 103, 64], [86, 124, 85], [51, 89, 50], [82, 120, 81], [66, 104, 65], [52, 90, 51], [71, 113, 74], [53, 91, 52], [84, 122, 83], [56, 96, 95], [54, 92, 53], [85, 123, 84], [61, 109, 70], [75, 117, 78], [55, 93, 54], [50, 96, 57], [70, 108, 69], [56, 94, 55], [87, 125, 86], [72, 110, 71], [59, 97, 58], [73, 111, 72], [58, 99, 60], [67, 106, 105], [74, 113, 112], [68, 107, 106], [76, 115, 114], [60, 99, 98], [77, 116, 115], [83, 122, 121], [62, 101, 100], [88, 127, 126], [78, 117, 116], [79, 118, 127], [63, 102, 101], [69, 108, 107], [80, 119, 118], [64, 103, 102], [81, 120, 119], [65, 104, 103], [86, 125, 124], [51, 90, 89], [82, 121, 120], [66, 105, 104], [52, 91, 90], [71, 110, 113], [53, 92, 91], [84, 123, 122], [56, 57, 96], [54, 93, 92], [85, 124, 123], [61, 100, 109], [75, 114, 117], [55, 94, 93], [50, 89, 96], [70, 109, 108], [56, 95, 94], [87, 126, 125], [72, 111, 110], [59, 98, 97], [73, 112, 111], [58, 97, 99], [134, 129, 128], [129, 136, 130], [130, 137, 131], [137, 132, 131], [138, 133, 132], [139, 128, 133], [140, 135, 134], [141, 136, 135], [136, 143, 137], [143, 138, 137], [144, 139, 138], [139, 140, 134], [146, 141, 140], [147, 142, 141], [148, 143, 142], [149, 144, 143], [150, 145, 144], [151, 140, 145], [152, 147, 146], [153, 148, 147], [154, 149, 148], [155, 150, 149], [150, 157, 151], [157, 146, 151], [158, 153, 152], [159, 154, 153], [160, 155, 154], [161, 156, 155], [162, 157, 156], [157, 158, 152], [164, 159, 158], [159, 166, 160], [166, 161, 160], [167, 162, 161], [168, 163, 162], [169, 158, 163], [164, 129, 165], [129, 166, 165], [130, 167, 166], [131, 168, 167], [132, 169, 168], [169, 128, 164], [134, 135, 129], [129, 135, 136], [130, 136, 137], [137, 138, 132], [138, 139, 133], [139, 134, 128], [140, 141, 135], [141, 142, 136], [136, 142, 143], [143, 144, 138], [144, 145, 139], [139, 145, 140], [146, 147, 141], [147, 148, 142], [148, 149, 143], [149, 150, 144], [150, 151, 145], [151, 146, 140], [152, 153, 147], [153, 154, 148], [154, 155, 149], [155, 156, 150], [150, 156, 157], [157, 152, 146], [158, 159, 153], [159, 160, 154], [160, 161, 155], [161, 162, 156], [162, 163, 157], [157, 163, 158], [164, 165, 159], [159, 165, 166], [166, 167, 161], [167, 168, 162], [168, 169, 163], [169, 164, 158], [164, 128, 129], [129, 130, 166], [130, 131, 167], [131, 132, 168], [132, 133, 169], [169, 133, 128]]
 



#hideTurtle()
speed(10)
setPenColor("Black")

r = 0
while True:
    tv = rotate_y(vertices, r)
    tv = rotate_x(tv, sin(r * 2)/3)
    tv = translate(tv, [0, 0, -7])
    
    
    pv = project_vertices(tv, projection_matrix)
    
    clean()
    render_triangles()

    r += 0.3
