from gturtle import *
from math import *


makeTurtle()

screen_size = 1500

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

projection_matrix = perspective_matrix(1, radians(120), 0.1, 100)


vertices = [[-0.484034, 0.020155, 2.606177], [0.484034, 0.020155, 2.606177], [0.103827, 0.15985, 2.669507], [-0.103827, 0.15985, 2.669507], [0.393837, 0.378491, 2.819262], [0.15625, 0.4375, 2.677667], [-0.15625, 0.4375, 2.677667], [-0.464863, 0.413575, 2.573598], [-0.393837, 0.378491, 2.819262], [0.464863, 0.413575, 2.573598], [0.633263, 0.24203, 2.595723], [-0.633263, 0.24203, 2.595723], [-0.320532, 0.114372, 2.837929], [0.320532, 0.114372, 2.837929], [0.0, 0.372944, 2.818923], [0.0, -0.859401, 2.720895], [0.0, -0.1875, 2.826104], [0.0, 0.455016, 2.644344], [0.0, 0.739405, 1.270727], [0.0, -0.248586, 1.33675], [-0.226815, -0.192583, 2.562887], [0.226815, -0.192583, 2.562887], [-0.380003, -0.961727, 2.528368], [0.586132, -0.069318, 2.600818], [0.832894, 0.398588, 2.654324], [-0.238492, 0.773072, 2.740525], [0.224125, 0.132533, 2.786681], [-0.096071, -0.81117, 2.732821], [0.0, -0.195312, 2.779229], [0.0, -0.140625, 2.771417], [-0.586132, -0.069318, 2.600818], [-0.832894, 0.398588, 2.654324], [-0.224831, 0.55252, 2.827993], [0.224831, 0.55252, 2.827993], [-0.12315, -0.178023, 2.804646], [0.0, -0.302549, 2.813348], [0.12315, -0.178023, 2.804646], [0.096071, -0.81117, 2.732821], [-0.324415, 0.390499, 2.836053], [-0.553093, 0.260929, 2.722846], [-0.414048, 0.075581, 2.734605], [0.197297, 0.296692, 2.790817], [-0.197297, 0.296692, 2.790817], [0.324415, 0.390499, 2.836053], [0.414048, 0.075581, 2.734605], [0.553093, 0.260929, 2.722846], [-0.224125, 0.132533, 2.786681], [-0.331326, 0.565155, 2.559914], [0.238492, 0.773072, 2.740525], [-0.785346, 0.119346, 2.447115], [0.785346, 0.119346, 2.447115], [0.0, 0.976525, 2.220001], [0.0, -0.955036, 2.436022], [0.0, -0.4861, 2.327788], [0.85475, 0.356817, 1.840843], [-0.852752, 0.400749, 1.582975], [-0.748555, -0.110008, 1.701538], [-0.214052, -0.41023, 2.371137], [0.380003, -0.961727, 2.528368], [0.214052, -0.41023, 2.371137], [-0.71398, 0.702071, 1.65921], [-0.476077, 0.899132, 2.158056], [0.476077, 0.899132, 2.158056], [0.331326, 0.565155, 2.559914], [-0.755597, 0.411716, 2.346116], [0.755597, 0.411716, 2.346116], [0.71398, 0.702071, 1.65921], [-0.394325, -0.238686, 1.695698], [0.394325, -0.238686, 1.695698], [-0.717301, -0.102008, 1.931494], [-1.381379, 0.178077, 1.542842], [-1.090323, 0.422107, 1.659628], [1.20797, 0.310146, 1.588322], [1.090323, 0.422107, 1.659628], [0.717301, -0.102008, 1.931494], [-1.147014, 0.048217, 1.591349], [0.73678, 0.072512, 1.794978], [-0.73678, 0.072512, 1.794978], [-0.85475, 0.356817, 1.840843], [-0.864912, 0.016082, 1.71497], [1.147014, 0.048217, 1.591349], [0.864912, 0.016082, 1.71497], [-1.20797, 0.310146, 1.588322], [-1.227002, 0.480829, 1.476402], [1.227002, 0.480829, 1.476402], [1.381379, 0.178077, 1.542842], [0.748555, -0.110008, 1.701538], [0.852752, 0.400749, 1.582975], [0.0, -1.0, 0.0], [0.7236, -0.447215, 0.52572], [-0.276385, -0.447215, 0.85064], [-0.894425, -0.447215, 0.0], [-0.276385, -0.447215, -0.85064], [0.7236, -0.447215, -0.52572], [0.276385, 0.447215, 0.85064], [-0.7236, 0.447215, 0.52572], [-0.7236, 0.447215, -0.52572], [0.276385, 0.447215, -0.85064], [0.894425, 0.447215, 0.0], [0.0, 1.0, 0.0], [1.879858, -0.500882, -0.626103], [1.879858, 0.500882, -0.626103], [2.475317, -0.500882, -0.193476], [2.475317, 0.500882, -0.193476], [2.247872, -0.500882, 0.506528], [2.247872, 0.500882, 0.506528], [1.511844, -0.500882, 0.506528], [1.511844, 0.500882, 0.506528], [1.284399, -0.500882, -0.193476], [1.284399, 0.500882, -0.193476], [0.0, 1.277585, -0.88], [0.762102, 1.277585, -0.44], [0.762102, 1.277585, 0.44], [0.0, 1.277585, 0.88], [-0.762102, 1.277585, 0.44], [-0.762102, 1.277585, -0.44], [0.0, 2.277585, 0.0], [1.25, 0.0, -2.250942], [1.125, 0.216506, -2.250942], [0.875, 0.216506, -2.250942], [0.75, 0.0, -2.250942], [0.875, -0.216506, -2.250942], [1.125, -0.216506, -2.250942], [0.625, 0.0, -3.333474], [0.5625, 0.216506, -3.225221], [0.4375, 0.216506, -3.008715], [0.375, 0.0, -2.900461], [0.4375, -0.216506, -3.008715], [0.5625, -0.216506, -3.225221], [-0.625, 0.0, -3.333474], [-0.5625, 0.216506, -3.225221], [-0.4375, 0.216506, -3.008715], [-0.375, 0.0, -2.900461], [-0.4375, -0.216506, -3.008715], [-0.5625, -0.216506, -3.225221], [-1.25, 0.0, -2.250942], [-1.125, 0.216506, -2.250942], [-0.875, 0.216506, -2.250942], [-0.75, 0.0, -2.250942], [-0.875, -0.216506, -2.250942], [-1.125, -0.216506, -2.250942], [-0.625, 0.0, -1.16841], [-0.5625, 0.216506, -1.276664], [-0.4375, 0.216506, -1.49317], [-0.375, 0.0, -1.601423], [-0.4375, -0.216506, -1.49317], [-0.5625, -0.216506, -1.276664], [0.625, 0.0, -1.16841], [0.5625, 0.216506, -1.276664], [0.4375, 0.216506, -1.49317], [0.375, 0.0, -1.601423], [0.4375, -0.216506, -1.49317], [0.5625, -0.216506, -1.276664], [-2.570135, -0.584273, 0.584273], [-2.570135, 0.584273, 0.584273], [-2.570135, -0.584273, -0.584273], [-2.570135, 0.584273, -0.584273], [-1.401588, -0.584273, 0.584273], [-1.401588, 0.584273, 0.584273], [-1.401588, -0.584273, -0.584273], [-1.401588, 0.584273, -0.584273], [1.964754, -2.75685, -0.0], [1.67217, -2.875686, -0.0], [1.421709, -2.821042, -0.0], [1.28023, -2.591722, -0.0], [1.991841, -2.569863, -0.0], [1.943551, -2.298283, -0.0], [1.775119, -2.059893, -0.0], [1.393755, -2.050639, -0.0], [1.16012, -2.231086, -0.0], [1.091143, -2.528233, -0.0], [1.189673, -2.895431, -0.0], [1.617764, -3.069072, -0.0], [1.963674, -2.947878, -0.0], [1.300505, -2.366091, -0.0], [1.561867, -2.184974, -0.0], [1.792701, -2.367282, -0.0], [0.90396, -2.095512, -0.0], [0.560015, -2.01206, -0.0], [0.180174, -2.262247, -0.0], [0.14022, -2.70568, -0.0], [0.359957, -3.005917, -0.0], [0.886938, -3.028039, -0.0], [0.87693, -2.841222, -0.0], [0.457538, -2.831428, -0.0], [0.316212, -2.522192, -0.0], [0.439939, -2.270239, -0.0], [0.66144, -2.203453, -0.0], [0.902519, -2.300825, -0.0], [-0.102542, -2.049511, -0.0], [-0.298249, -2.049511, -0.0], [-0.298249, -3.03684, -0.0], [-0.102542, -3.03684, -0.0], [-0.239166, -1.628829, -0.0], [-0.32092, -1.790324, -0.0], [-0.159425, -1.872078, -0.0], [-0.077671, -1.710582, -0.0], [-0.606102, -1.537155, -0.0], [-0.808405, -1.537155, -0.0], [-0.808405, -2.698202, -0.0], [-1.941362, -1.513321, -0.0], [-1.995839, -3.03684, -0.0], [-1.793536, -3.03684, -0.0], [-1.793536, -1.88239, -0.0], [-0.665085, -3.062456, -0.0], [1.964754, -2.75685, 0.24562], [1.67217, -2.875686, 0.24562], [1.421709, -2.821042, 0.24562], [1.28023, -2.591722, 0.24562], [1.991841, -2.569863, 0.24562], [1.943551, -2.298283, 0.24562], [1.775119, -2.059893, 0.24562], [1.393755, -2.050639, 0.24562], [1.16012, -2.231086, 0.24562], [1.091143, -2.528233, 0.24562], [1.189673, -2.895431, 0.24562], [1.617764, -3.069072, 0.24562], [1.963674, -2.947878, 0.24562], [1.300505, -2.366091, 0.24562], [1.561867, -2.184974, 0.24562], [1.792701, -2.367282, 0.24562], [0.90396, -2.095512, 0.24562], [0.560015, -2.01206, 0.24562], [0.180174, -2.262247, 0.24562], [0.14022, -2.70568, 0.24562], [0.359957, -3.005917, 0.24562], [0.886938, -3.028039, 0.24562], [0.87693, -2.841222, 0.24562], [0.457538, -2.831428, 0.24562], [0.316212, -2.522192, 0.24562], [0.439939, -2.270239, 0.24562], [0.66144, -2.203453, 0.24562], [0.902519, -2.300825, 0.24562], [-0.102542, -2.049511, 0.24562], [-0.298249, -2.049511, 0.24562], [-0.298249, -3.03684, 0.24562], [-0.102542, -3.03684, 0.24562], [-0.239166, -1.628829, 0.24562], [-0.32092, -1.790324, 0.24562], [-0.159425, -1.872078, 0.24562], [-0.077671, -1.710582, 0.24562], [-0.606102, -1.537155, 0.24562], [-0.808405, -1.537155, 0.24562], [-0.808405, -2.698202, 0.24562], [-1.941362, -1.513321, 0.24562], [-1.995839, -3.03684, 0.24562], [-1.793536, -3.03684, 0.24562], [-1.793536, -1.88239, 0.24562], [-0.665085, -3.062456, 0.24562]]
faces = [[4, 13, 10], [12, 8, 11], [13, 4, 2], [8, 12, 3], [8, 3, 6], [8, 6, 7], [10, 9, 4], [21, 23, 36], [30, 20, 34], [24, 23, 50], [25, 31, 32], [14, 33, 48], [24, 33, 45], [30, 39, 31], [36, 23, 26], [26, 14, 36], [14, 46, 34], [32, 42, 14], [46, 14, 42], [37, 15, 58], [15, 27, 22], [36, 37, 58], [27, 34, 22], [36, 15, 37], [34, 15, 35], [16, 29, 28], [16, 29, 34], [29, 36, 14], [34, 29, 14], [23, 45, 44], [39, 30, 40], [32, 39, 38], [41, 43, 33], [14, 63, 17], [47, 14, 17], [24, 63, 48], [31, 47, 64], [50, 65, 24], [53, 58, 52], [53, 22, 57], [20, 30, 49], [56, 19, 67], [19, 59, 53], [57, 19, 53], [50, 74, 54], [69, 49, 78], [87, 19, 18], [55, 19, 56], [51, 66, 18], [60, 51, 18], [62, 65, 66], [64, 61, 60], [63, 51, 17], [47, 51, 61], [49, 64, 78], [54, 66, 65], [60, 78, 64], [66, 54, 87], [50, 68, 74], [67, 49, 69], [50, 21, 68], [20, 49, 67], [21, 59, 68], [67, 57, 20], [68, 86, 74], [71, 70, 82], [82, 70, 75], [80, 74, 85], [74, 81, 76], [79, 69, 77], [78, 71, 77], [69, 78, 77], [80, 81, 74], [81, 72, 73], [82, 79, 71], [81, 73, 76], [71, 79, 77], [82, 75, 79], [85, 84, 73], [73, 84, 54], [78, 55, 83], [86, 87, 84], [84, 85, 86], [70, 83, 56], [10, 13, 1], [0, 12, 11], [1, 13, 2], [3, 12, 0], [4, 5, 2], [4, 9, 5], [11, 8, 7], [21, 36, 58], [22, 34, 20], [31, 49, 30], [48, 33, 24], [14, 25, 32], [31, 39, 32], [23, 24, 45], [34, 46, 30], [33, 14, 41], [26, 41, 14], [36, 35, 15], [34, 27, 15], [16, 36, 29], [16, 35, 36], [34, 35, 16], [26, 23, 44], [40, 30, 46], [33, 43, 45], [42, 32, 38], [14, 48, 63], [47, 25, 14], [24, 65, 63], [31, 25, 47], [49, 31, 64], [53, 59, 58], [53, 52, 22], [58, 15, 52], [52, 15, 22], [21, 58, 59], [57, 22, 20], [21, 50, 23], [86, 68, 19], [19, 68, 59], [57, 67, 19], [87, 86, 19], [55, 18, 19], [51, 62, 66], [60, 61, 51], [18, 66, 87], [55, 60, 18], [62, 63, 65], [64, 47, 61], [63, 62, 51], [47, 17, 51], [50, 54, 65], [60, 55, 78], [67, 69, 56], [73, 72, 85], [72, 80, 85], [75, 70, 69], [54, 76, 73], [74, 76, 54], [75, 69, 79], [72, 81, 80], [85, 74, 86], [56, 69, 70], [70, 71, 83], [71, 78, 83], [54, 84, 87], [56, 83, 55], [88, 89, 90], [89, 88, 93], [88, 90, 91], [88, 91, 92], [88, 92, 93], [89, 93, 98], [90, 89, 94], [91, 90, 95], [92, 91, 96], [93, 92, 97], [89, 98, 94], [90, 94, 95], [91, 95, 96], [92, 96, 97], [93, 97, 98], [94, 98, 99], [95, 94, 99], [96, 95, 99], [97, 96, 99], [98, 97, 99], [101, 102, 100], [103, 104, 102], [105, 106, 104], [101, 107, 105], [107, 108, 106], [109, 100, 108], [102, 106, 108], [110, 116, 111], [111, 116, 112], [112, 116, 113], [113, 116, 114], [111, 113, 115], [114, 116, 115], [115, 116, 110], [123, 118, 117], [124, 119, 118], [125, 120, 119], [126, 121, 120], [121, 128, 122], [122, 123, 117], [129, 124, 123], [130, 125, 124], [131, 126, 125], [132, 127, 126], [127, 134, 128], [134, 123, 128], [135, 130, 129], [136, 131, 130], [137, 132, 131], [138, 133, 132], [139, 134, 133], [134, 135, 129], [141, 136, 135], [142, 137, 136], [137, 144, 138], [144, 139, 138], [145, 140, 139], [140, 141, 135], [147, 142, 141], [142, 149, 143], [149, 144, 143], [150, 145, 144], [151, 146, 145], [152, 141, 146], [117, 148, 147], [118, 149, 148], [119, 150, 149], [150, 121, 151], [121, 152, 151], [122, 147, 152], [154, 155, 153], [156, 159, 155], [160, 157, 159], [158, 153, 157], [159, 153, 155], [156, 158, 160], [169, 168, 167], [175, 169, 167], [175, 167, 166], [169, 175, 174], [176, 175, 166], [176, 166, 165], [170, 169, 174], [170, 174, 176], [170, 176, 165], [164, 170, 165], [171, 170, 164], [171, 164, 163], [162, 161, 173], [171, 163, 162], [171, 162, 173], [171, 173, 172], [179, 178, 177], [179, 177, 187], [187, 177, 188], [179, 187, 186], [179, 186, 185], [180, 179, 185], [180, 185, 184], [181, 180, 184], [181, 184, 183], [181, 183, 182], [194, 193, 196], [194, 196, 195], [191, 190, 189], [191, 189, 192], [201, 200, 203], [203, 200, 199], [199, 198, 197], [199, 197, 204], [201, 203, 202], [204, 203, 199], [213, 211, 212], [219, 211, 213], [219, 210, 211], [213, 218, 219], [220, 210, 219], [220, 209, 210], [214, 218, 213], [214, 220, 218], [214, 209, 220], [208, 209, 214], [215, 208, 214], [215, 207, 208], [206, 217, 205], [215, 206, 207], [215, 217, 206], [215, 216, 217], [223, 221, 222], [223, 231, 221], [231, 232, 221], [223, 230, 231], [223, 229, 230], [224, 229, 223], [224, 228, 229], [225, 228, 224], [225, 227, 228], [225, 226, 227], [238, 240, 237], [238, 239, 240], [235, 233, 234], [235, 236, 233], [245, 247, 244], [247, 243, 244], [243, 241, 242], [243, 248, 241], [245, 246, 247], [248, 243, 247], [173, 216, 172], [190, 233, 189], [192, 235, 191], [164, 207, 163], [186, 229, 185], [163, 206, 162], [161, 217, 173], [189, 236, 192], [166, 209, 165], [201, 244, 200], [171, 214, 170], [200, 243, 199], [203, 246, 202], [170, 213, 169], [172, 215, 171], [168, 211, 167], [204, 247, 203], [174, 220, 176], [193, 240, 196], [167, 210, 166], [194, 237, 193], [175, 218, 174], [176, 219, 175], [177, 232, 188], [169, 212, 168], [180, 223, 179], [178, 221, 177], [197, 248, 204], [182, 225, 181], [185, 228, 184], [195, 238, 194], [179, 222, 178], [162, 205, 161], [196, 239, 195], [181, 224, 180], [165, 208, 164], [191, 234, 190], [198, 241, 197], [183, 226, 182], [184, 227, 183], [199, 242, 198], [187, 230, 186], [202, 245, 201], [188, 231, 187], [101, 103, 102], [103, 105, 104], [105, 107, 106], [105, 103, 101], [101, 109, 107], [107, 109, 108], [109, 101, 100], [108, 100, 102], [102, 104, 106], [115, 110, 111], [111, 112, 113], [113, 114, 115], [123, 124, 118], [124, 125, 119], [125, 126, 120], [126, 127, 121], [121, 127, 128], [122, 128, 123], [129, 130, 124], [130, 131, 125], [131, 132, 126], [132, 133, 127], [127, 133, 134], [134, 129, 123], [135, 136, 130], [136, 137, 131], [137, 138, 132], [138, 139, 133], [139, 140, 134], [134, 140, 135], [141, 142, 136], [142, 143, 137], [137, 143, 144], [144, 145, 139], [145, 146, 140], [140, 146, 141], [147, 148, 142], [142, 148, 149], [149, 150, 144], [150, 151, 145], [151, 152, 146], [152, 147, 141], [117, 118, 148], [118, 119, 149], [119, 120, 150], [150, 120, 121], [121, 122, 152], [122, 117, 147], [154, 156, 155], [156, 160, 159], [160, 158, 157], [158, 154, 153], [159, 157, 153], [156, 154, 158], [173, 217, 216], [190, 234, 233], [192, 236, 235], [164, 208, 207], [186, 230, 229], [163, 207, 206], [161, 205, 217], [189, 233, 236], [166, 210, 209], [201, 245, 244], [171, 215, 214], [200, 244, 243], [203, 247, 246], [170, 214, 213], [172, 216, 215], [168, 212, 211], [204, 248, 247], [174, 218, 220], [193, 237, 240], [167, 211, 210], [194, 238, 237], [175, 219, 218], [176, 220, 219], [177, 221, 232], [169, 213, 212], [180, 224, 223], [178, 222, 221], [197, 241, 248], [182, 226, 225], [185, 229, 228], [195, 239, 238], [179, 223, 222], [162, 206, 205], [196, 240, 239], [181, 225, 224], [165, 209, 208], [191, 235, 234], [198, 242, 241], [183, 227, 226], [184, 228, 227], [199, 243, 242], [187, 231, 230], [202, 246, 245], [188, 232, 231]]
 



hideTurtle()
#speed(1000)
setPenColor("Black")

r = 0
while True:
    tv = rotate_y(vertices, r)
    tv = rotate_x(tv, sin(r * 2)/3)
    tv = translate(tv, [0, 0, -7])
    
    
    pv = project_vertices(tv, projection_matrix)
    
    clean()
    for i in sorted(faces, key=poly_sort):
        pos = [pv[i[0]], pv[i[1]], pv[i[2]]]
        avpos = div(add(add(tv[i[0]], tv[i[1]]), tv[i[2]]), 3)
        dif = max(dot_product(compute_normal([tv[i[0]], tv[i[1]], tv[i[2]]]), normalize(avpos)), 0.0)
        
        if dif > 0:
            dif = dif * 0.7 + 0.2
            color = (dif, 0, 0)
            setFillColor(color)
            setPenColor(color)
            draw_triangle(pos)

    delay(0)
    r += 0.01