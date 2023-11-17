import pygame
from math import *
from output import *

screen = pygame.display.set_mode((1000, 1000))


screen_size = 1000



def matrix_multiply(matrix, vector):
    result = [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]
    return result
    
def dot_product(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))
    
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
        projected_vertices.append([projected_vertex[0]*scale +  screen_size/2, -projected_vertex[1]*scale +  screen_size/2, projected_vertex[2]])
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
    


def poly_sort(poly):
    return -(pv[poly[0][0]][2] + pv[poly[1][0]][2] + pv[poly[2][0]][2]) / 3

projection_matrix = perspective_matrix(1, radians(90), 0.1, 100)


r = 0
while True:
    transformed_vertices = rotate_y(vertices, r)
    transformed_vertices = rotate_x(transformed_vertices, sin(r*2))
    


    transformed_vertices = translate(transformed_vertices, [0, 0, -7])
    
    camera_pos = [cos(r + pi/2), 0, sin(r + pi/2)]
    
    pv = project_vertices(transformed_vertices, projection_matrix)
    screen.fill((255, 255, 255))

    for i in sorted(faces, key=poly_sort):
        pos = [pv[i[0][0]][:2], pv[i[1][0]][:2], pv[i[2][0]][:2]]
        dif = max(dot_product(normals[i[0][1]], [0, 0, 1]), 0.0) * 200
        
        color = (0, dif, dif)

        pygame.draw.polygon(screen, color, pos, 0)
    pygame.display.update()
    r += 0.01
