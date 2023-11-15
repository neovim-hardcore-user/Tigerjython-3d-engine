import pygame
from math import *

screen = pygame.display.set_mode((1000, 1000))


screen_size = 1000


def matrix_multiply(matrix, vector):
    result = [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]
    return result
    

    
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




def project_vertices(vertices, projection_matrix):
    projected_vertices = []
    for vertex in vertices:
        projected_vertex = matrix_multiply(projection_matrix, vertex + [1])
        scale = (1 / projected_vertex[3]) * screen_size
        projected_vertices.append([projected_vertex[0]*scale +  screen_size/2, -projected_vertex[1]*scale +  screen_size/2])
    return projected_vertices

def translate(vertices, translation_vector):
    translation_matrix_ = translation_matrix(translation_vector)
    translated_vertices = [matrix_multiply(translation_matrix_, vertex + [1])[:3] for vertex in vertices]
    return translated_vertices

def scale(vertices, scale_vector):
    scale_matrix_ = scale_matrix(scale_vector)
    scaled_vertices = [matrix_multiply(scale_matrix_, vertex + [1])[:3] for vertex in vertices]
    return scaled_vertices
    
def rotate(vertices, angles):
    rx, ry, rz = map(radians, angles)
    rotation_matrix_x_ = rotation_matrix_x(rx)
    rotation_matrix_y_ = rotation_matrix_y(ry)
    rotation_matrix_z_ = rotation_matrix_z(rz)

    for i in range(len(vertices)):
        rotated_vertex = matrix_multiply(rotation_matrix_x_, vertices[i] + [1])
        rotated_vertex = matrix_multiply(rotation_matrix_y_, rotated_vertex)
        rotated_vertex = matrix_multiply(rotation_matrix_z_, rotated_vertex)
        vertices[i] = rotated_vertex[:3]

    return vertices

def poly_sort(poly):
    return (transformed_vertices[poly[0][0]][2] + transformed_vertices[poly[1][0]][2] + transformed_vertices[poly[2][0]][2]) / 3

projection_matrix = perspective_matrix(1, radians(90), 0.1, 100)


vertices = [[-2.204134, -1.0, 0.0], [-1.480534, -0.447215, 0.52572], [-2.480519, -0.447215, 0.85064], [-3.098559, -0.447215, 0.0], [-2.480519, -0.447215, -0.85064], [-1.480534, -0.447215, -0.52572], [-1.927749, 0.447215, 0.85064], [-2.927734, 0.447215, 0.52572], [-2.927734, 0.447215, -0.52572], [-1.927749, 0.447215, -0.85064], [-1.309709, 0.447215, 0.0], [-2.204134, 1.0, 0.0], [-0.484034, 0.020155, 0.576947], [0.484034, 0.020155, 0.576947], [0.103827, 0.15985, 0.640278], [-0.103827, 0.15985, 0.640278], [0.393837, 0.378491, 0.790033], [0.15625, 0.4375, 0.648438], [-0.15625, 0.4375, 0.648438], [-0.464863, 0.413575, 0.544369], [-0.393837, 0.378491, 0.790033], [0.464863, 0.413575, 0.544369], [0.633263, 0.24203, 0.566494], [-0.633263, 0.24203, 0.566494], [-0.320532, 0.114372, 0.8087], [0.320532, 0.114372, 0.8087], [0.0, -0.859401, 0.691666], [0.0, -0.1875, 0.796875], [0.0, 0.367889, 0.758962], [0.0, 0.739405, -0.758502], [0.0, -0.248586, -0.692479], [-0.258974, -0.3156, 0.417902], [-0.380003, -0.961727, 0.499138], [0.750929, 0.043677, 0.516782], [0.832894, 0.398588, 0.625095], [-0.238492, 0.773072, 0.711296], [0.224125, 0.132533, 0.757452], [-0.096071, -0.81117, 0.703592], [0.0, -0.195312, 0.75], [0.0, -0.140625, 0.742188], [-0.750929, 0.043677, 0.516782], [-0.832894, 0.398588, 0.625095], [-0.224831, 0.55252, 0.798764], [0.224831, 0.55252, 0.798764], [-0.12315, -0.178023, 0.775416], [0.0, -0.302549, 0.784118], [0.12315, -0.178023, 0.775416], [0.096071, -0.81117, 0.703592], [-0.308957, 0.38547, 0.812405], [-0.553093, 0.260929, 0.693617], [-0.414048, 0.075581, 0.705376], [0.308957, 0.38547, 0.812405], [0.414048, 0.075581, 0.705376], [0.553093, 0.260929, 0.693617], [-0.224125, 0.132533, 0.757452], [-0.331326, 0.565155, 0.530685], [0.238492, 0.773072, 0.711296], [0.0, 0.976525, 0.190772], [0.0, -0.955036, 0.406793], [0.0, -0.4861, 0.298559], [-0.911953, 0.420039, -0.321816], [-0.647815, -0.09471, -0.356679], [0.380003, -0.961727, 0.499138], [0.258974, -0.3156, 0.417902], [-0.707038, 0.797508, -0.22044], [0.707038, 0.797508, -0.22044], [0.331326, 0.565155, 0.530685], [-0.755597, 0.411716, 0.316887], [0.755597, 0.411716, 0.316887], [-0.717301, -0.102008, -0.097735], [-1.279217, 0.168899, -0.468389], [0.717301, -0.102008, -0.097735], [-0.801454, 0.038871, -0.291673], [1.279217, 0.168899, -0.468389], [0.801454, 0.038871, -0.291673], [-1.151718, 0.460262, -0.412947], [1.151718, 0.460262, -0.412947], [0.647815, -0.09471, -0.356679], [0.911953, 0.420039, -0.321816], [1.676328, -0.709274, 0.709274], [1.676328, 0.709274, 0.709274], [1.676328, -0.709274, -0.709274], [1.676328, 0.709274, -0.709274], [3.094877, -0.709274, 0.709274], [3.094877, 0.709274, 0.709274], [3.094877, -0.709274, -0.709274], [3.094877, 0.709274, -0.709274]]
normals = [[0.1876, -0.7947, 0.5774], [0.6071, -0.7947, -0.0], [-0.4911, -0.7947, 0.3568], [-0.4911, -0.7947, -0.3568], [0.1876, -0.7947, -0.5774], [0.9822, -0.1876, -0.0], [0.3035, -0.1876, 0.9342], [-0.7946, -0.1876, 0.5774], [-0.7946, -0.1876, -0.5774], [0.3035, -0.1876, -0.9342], [0.7946, 0.1876, 0.5774], [-0.3035, 0.1876, 0.9342], [-0.9822, 0.1876, -0.0], [-0.3035, 0.1876, -0.9342], [0.7946, 0.1876, -0.5774], [0.4911, 0.7947, 0.3568], [-0.1876, 0.7947, 0.5774], [-0.6071, 0.7947, -0.0], [-0.1876, 0.7947, -0.5774], [0.4911, 0.7947, -0.3568], [0.6387, -0.1236, 0.7595], [-0.6387, -0.1236, 0.7595], [-0.5709, 0.2145, 0.7925], [0.5709, 0.2145, 0.7925], [0.4981, 0.0686, 0.8644], [-0.1357, 0.9746, 0.1784], [0.6639, 0.6892, 0.2904], [0.459, -0.7567, 0.4656], [-0.459, -0.7567, 0.4656], [-0.3354, 0.3293, 0.8826], [-0.4376, 0.3548, 0.8262], [0.2619, -0.0527, 0.9637], [-0.3814, -0.3493, 0.8559], [0.4033, -0.0784, 0.9117], [0.0502, 0.0414, 0.9979], [-0.0502, 0.0414, 0.9979], [0.1702, -0.0052, 0.9854], [0.1596, -0.1582, 0.9744], [0.2165, -0.6181, 0.7557], [-0.2165, -0.6181, 0.7557], [0.5384, -0.1177, 0.8344], [-0.5384, -0.1177, 0.8344], [-0.0681, -0.1096, 0.9916], [-0.2291, -0.1594, 0.9603], [-1.0, -0.0, -0.0], [-0.0549, 0.7581, 0.6498], [-0.2694, -0.0318, 0.9625], [0.2694, -0.0318, 0.9625], [0.4481, -0.2824, 0.8482], [-0.4481, -0.2824, 0.8482], [-0.5454, 0.3373, 0.7673], [0.3495, 0.6985, -0.6245], [-0.3218, 0.946, -0.0404], [0.9581, -0.146, -0.2465], [0.2268, -0.219, -0.949], [-0.4354, -0.0316, -0.8997], [0.5988, -0.7789, -0.1867], [-0.5988, -0.7789, -0.1867], [0.9406, -0.3384, 0.0287], [-0.9406, -0.3384, 0.0287], [0.4137, -0.0607, -0.9084], [-0.4872, -0.1923, -0.8518], [0.1041, 0.9649, -0.241], [-0.1041, 0.9649, -0.241], [0.0969, 0.6792, 0.7275], [-0.4616, 0.7557, 0.4646], [-0.9643, 0.1168, 0.2376], [0.8808, 0.4188, 0.2211], [-0.8808, 0.4188, 0.2211], [-0.765, -0.6161, 0.1879], [0.765, -0.6161, 0.1879], [0.5808, -0.8118, 0.0601], [-0.5808, -0.8118, 0.0601], [-0.3596, -0.0305, 0.9326], [-0.9409, -0.2551, 0.2229], [-0.0033, 0.8098, 0.5868], [0.3525, -0.0238, 0.9355], [-0.3525, -0.0238, 0.9355], [-0.3807, 0.2555, -0.8887], [-0.2109, 0.0929, -0.9731], [0.2109, 0.0929, -0.9731], [0.6571, -0.4122, 0.6311], [-0.6571, -0.4122, 0.6311], [-0.3176, -0.9353, 0.1561], [0.3176, -0.9353, 0.1561], [-0.4981, 0.0686, 0.8644], [0.1357, 0.9746, 0.1784], [-0.6639, 0.6892, 0.2904], [0.938, 0.2103, 0.2754], [-0.938, 0.2103, 0.2754], [0.3354, 0.3293, 0.8826], [0.4376, 0.3548, 0.8262], [-0.2619, -0.0527, 0.9637], [0.3814, -0.3493, 0.8559], [-0.4033, -0.0784, 0.9117], [-0.1702, -0.0052, 0.9854], [-0.1596, -0.1582, 0.9744], [0.2291, -0.1594, 0.9603], [0.0681, -0.1096, 0.9916], [0.0549, 0.7581, 0.6498], [0.1787, -0.1084, 0.9779], [-0.1787, -0.1084, 0.9779], [-0.3742, -0.7532, -0.541], [0.3742, -0.7532, -0.541], [0.5454, 0.3373, 0.7673], [-0.6569, 0.3055, -0.6893], [0.6569, 0.3055, -0.6893], [0.3218, 0.946, -0.0404], [-0.3495, 0.6985, -0.6245], [-0.9581, -0.146, -0.2465], [0.4354, -0.0316, -0.8997], [-0.2268, -0.219, -0.949], [-0.0936, -0.9438, 0.3169], [0.0936, -0.9438, 0.3169], [0.2901, -0.9488, -0.1249], [-0.2901, -0.9488, -0.1249], [0.4872, -0.1923, -0.8518], [-0.4137, -0.0607, -0.9084], [0.5097, 0.4702, -0.7205], [-0.5097, 0.4702, -0.7205], [0.5009, 0.7239, 0.4745], [-0.5009, 0.7239, 0.4745], [0.4616, 0.7557, 0.4646], [-0.0969, 0.6792, 0.7275], [0.9643, 0.1168, 0.2376], [0.3596, -0.0305, 0.9326], [0.9409, -0.2551, 0.2229], [0.0033, 0.8098, 0.5868], [0.3636, -0.9233, -0.1236], [-0.3636, -0.9233, -0.1236], [0.3807, 0.2555, -0.8887], [-1.0, -0.0, -0.0], [-0.0, -0.0, -1.0], [1.0, -0.0, -0.0], [-0.0, -0.0, 1.0], [-0.0, -1.0, -0.0], [-0.0, 1.0, -0.0]]
faces = [[[0, 0], [1, 0], [2, 0]], [[1, 1], [0, 1], [5, 1]], [[0, 2], [2, 2], [3, 2]], [[0, 3], [3, 3], [4, 3]], [[0, 4], [4, 4], [5, 4]], [[1, 5], [5, 5], [10, 5]], [[2, 6], [1, 6], [6, 6]], [[3, 7], [2, 7], [7, 7]], [[4, 8], [3, 8], [8, 8]], [[5, 9], [4, 9], [9, 9]], [[1, 10], [10, 10], [6, 10]], [[2, 11], [6, 11], [7, 11]], [[3, 12], [7, 12], [8, 12]], [[4, 13], [8, 13], [9, 13]], [[5, 14], [9, 14], [10, 14]], [[6, 15], [10, 15], [11, 15]], [[7, 16], [6, 16], [11, 16]], [[8, 17], [7, 17], [11, 17]], [[9, 18], [8, 18], [11, 18]], [[10, 19], [9, 19], [11, 19]], [[16, 20], [25, 20], [22, 20]], [[24, 21], [20, 21], [23, 21]], [[25, 22], [16, 22], [14, 22]], [[20, 23], [24, 23], [15, 23]], [[20, 24], [15, 24], [18, 24]], [[20, 25], [18, 25], [19, 25]], [[22, 26], [21, 26], [16, 26]], [[63, 27], [33, 27], [46, 27]], [[40, 28], [31, 28], [44, 28]], [[35, 29], [41, 29], [42, 29]], [[28, 30], [43, 30], [56, 30]], [[34, 31], [43, 31], [53, 31]], [[40, 32], [49, 32], [41, 32]], [[46, 33], [33, 33], [36, 33]], [[36, 34], [28, 34], [46, 34]], [[28, 35], [54, 35], [44, 35]], [[42, 36], [48, 36], [28, 36]], [[54, 37], [28, 37], [48, 37]], [[47, 38], [26, 38], [62, 38]], [[26, 39], [37, 39], [32, 39]], [[46, 40], [47, 40], [62, 40]], [[37, 41], [44, 41], [32, 41]], [[46, 42], [26, 42], [47, 42]], [[44, 43], [26, 43], [45, 43]], [[27, 44], [39, 44], [38, 44]], [[27, 45], [39, 45], [44, 45]], [[39, 46], [46, 46], [28, 46]], [[44, 47], [39, 47], [28, 47]], [[33, 48], [53, 48], [52, 48]], [[49, 49], [40, 49], [50, 49]], [[42, 50], [49, 50], [48, 50]], [[34, 51], [66, 51], [56, 51]], [[41, 52], [55, 52], [67, 52]], [[33, 53], [68, 53], [34, 53]], [[59, 54], [62, 54], [58, 54]], [[59, 55], [32, 55], [31, 55]], [[30, 56], [63, 56], [59, 56]], [[31, 57], [30, 57], [59, 57]], [[33, 58], [71, 58], [78, 58]], [[69, 59], [40, 59], [60, 59]], [[78, 60], [30, 60], [29, 60]], [[60, 61], [30, 61], [61, 61]], [[57, 62], [65, 62], [29, 62]], [[64, 63], [57, 63], [29, 63]], [[66, 64], [57, 64], [28, 64]], [[55, 65], [57, 65], [64, 65]], [[40, 66], [67, 66], [60, 66]], [[78, 67], [65, 67], [68, 67]], [[64, 68], [60, 68], [67, 68]], [[33, 69], [77, 69], [71, 69]], [[61, 70], [40, 70], [69, 70]], [[33, 71], [63, 71], [77, 71]], [[31, 72], [40, 72], [61, 72]], [[60, 73], [75, 73], [72, 73]], [[69, 74], [60, 74], [72, 74]], [[73, 75], [74, 75], [71, 75]], [[74, 76], [73, 76], [76, 76]], [[70, 77], [72, 77], [75, 77]], [[77, 78], [78, 78], [76, 78]], [[76, 79], [73, 79], [77, 79]], [[70, 80], [75, 80], [61, 80]], [[22, 81], [25, 81], [13, 81]], [[12, 82], [24, 82], [23, 82]], [[13, 83], [25, 83], [14, 83]], [[15, 84], [24, 84], [12, 84]], [[16, 85], [17, 85], [14, 85]], [[16, 86], [21, 86], [17, 86]], [[23, 87], [20, 87], [19, 87]], [[63, 88], [46, 88], [62, 88]], [[32, 89], [44, 89], [31, 89]], [[56, 90], [43, 90], [34, 90]], [[28, 91], [35, 91], [42, 91]], [[41, 92], [49, 92], [42, 92]], [[33, 93], [34, 93], [53, 93]], [[44, 94], [54, 94], [40, 94]], [[43, 95], [28, 95], [51, 95]], [[36, 96], [51, 96], [28, 96]], [[46, 97], [45, 97], [26, 97]], [[44, 98], [37, 98], [26, 98]], [[27, 99], [46, 99], [39, 99]], [[27, 100], [45, 100], [46, 100]], [[44, 101], [45, 101], [27, 101]], [[36, 102], [33, 102], [52, 102]], [[50, 103], [40, 103], [54, 103]], [[43, 104], [51, 104], [53, 104]], [[28, 105], [56, 105], [66, 105]], [[55, 106], [35, 106], [28, 106]], [[34, 107], [68, 107], [66, 107]], [[41, 108], [35, 108], [55, 108]], [[40, 109], [41, 109], [67, 109]], [[59, 110], [63, 110], [62, 110]], [[59, 111], [58, 111], [32, 111]], [[62, 112], [26, 112], [58, 112]], [[58, 113], [26, 113], [32, 113]], [[30, 114], [77, 114], [63, 114]], [[31, 115], [61, 115], [30, 115]], [[78, 116], [77, 116], [30, 116]], [[60, 117], [29, 117], [30, 117]], [[29, 118], [65, 118], [78, 118]], [[60, 119], [64, 119], [29, 119]], [[65, 120], [66, 120], [68, 120]], [[67, 121], [55, 121], [64, 121]], [[66, 122], [65, 122], [57, 122]], [[55, 123], [28, 123], [57, 123]], [[33, 124], [78, 124], [68, 124]], [[78, 125], [74, 125], [76, 125]], [[71, 126], [74, 126], [78, 126]], [[70, 127], [69, 127], [72, 127]], [[73, 128], [71, 128], [77, 128]], [[61, 129], [69, 129], [70, 129]], [[61, 130], [75, 130], [60, 130]], [[80, 131], [81, 131], [79, 131]], [[82, 132], [85, 132], [81, 132]], [[86, 133], [83, 133], [85, 133]], [[84, 134], [79, 134], [83, 134]], [[85, 135], [79, 135], [81, 135]], [[82, 136], [84, 136], [86, 136]], [[80, 131], [82, 131], [81, 131]], [[82, 132], [86, 132], [85, 132]], [[86, 133], [84, 133], [83, 133]], [[84, 134], [80, 134], [79, 134]], [[85, 135], [83, 135], [79, 135]], [[82, 136], [80, 136], [84, 136]]]
 





r = 0
while True:
    transformed_vertices = scale(vertices, [1, 1, 1])
    transformed_vertices = rotate(transformed_vertices, [0.0, r*10, 0.0])
    transformed_vertices = translate(transformed_vertices, [0, 0, -7])
    
    faces.sort(key = poly_sort)
    
    pv = project_vertices(transformed_vertices, projection_matrix)
    
        
    screen.fill((255, 255, 255))

    for i in faces:
        pos = [pv[i[0][0]], pv[i[1][0]], pv[i[2][0]]]
        color = ((normals[i[1][1]][0]/2 + 0.5)*255, (normals[i[1][1]][1]/2 + 0.5)*255, (normals[i[1][1]][2]/2 + 0.5)*255)

        pygame.draw.polygon(screen, color, pos, 0)


    pygame.display.update()
    r += 0.5
