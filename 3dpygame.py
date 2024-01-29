import pygame
from math import *
from hm import *


screen = pygame.display.set_mode((1600, 900))




def matrix_multiply(mat1, mat2):
    return [[sum(mat1[i][k] * mat2[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


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
    return (pos[2][1] - pos[0][1]) * (pos[1][0] - pos[0][0]) < (pos[1][1] - pos[0][1]) * (pos[2][0] - pos[0][0])

def poly_sort(poly):
    return -(tranf_verts[poly[0]][2] + tranf_verts[poly[1]][2] + tranf_verts[poly[2]][2])

projection_matrix = perspective_matrix(1, radians(110), 0.01, 100, screen.get_size()[1])
projection_matrix = matrix_multiply(projection_matrix, scale_matrix([1, -1, 1]))

screen_size = list(screen.get_size()) + [0]
t = 0
while True:
    tranf_mat = matrix_multiply(projection_matrix, translation_matrix([0, 0, -7]))
    tranf_mat = matrix_multiply(tranf_mat, rotation_matrix_x(sin(t*2)/2))
    tranf_mat = matrix_multiply(tranf_mat, rotation_matrix_y(t))

    tranf_verts = []
    for vertex in vertices:
        vert = matrix_vector_multiply(tranf_mat, vertex + [1])
        tranf_verts.append([vert[v] / vert[3] + screen_size[v]/2 for v in range(0, 3)])
    
        
    screen.fill((255, 255, 255))
    for face in sorted(faces, key=poly_sort):
        pos = [tranf_verts[face[tri]][:2] for tri in range(0, 3)]
        
        if is_visible(pos):
            color = [(n*0.5+0.5) * 255 for n in normals[face[3]]]
            pygame.draw.polygon(screen, color, pos, 0)

    pygame.display.update()
    t += 0.05
