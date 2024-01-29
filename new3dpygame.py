### general import stuff

import pygame
from math import *
from time import *


### matrix and vector math

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
    
def length(vector):
    return sqrt(sum(x * x for x in vector))    

def normalize(vector):
    l = length(vector)
    return [x / l for x in vector] if l != 0 else vector




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
    
def transform_vertices(vertices, tranf_mat):
    tranf_verts = []
    for vertex in vertices:
        vert = matrix_vector_multiply(tranf_mat, vertex + [1])
        tranf_verts.append([vert[v] / vert[3] for v in range(0, 2)] + [vert[2]])
        
    return tranf_verts
    
def is_frontfacing(pos):
    return (pos[2][1] - pos[0][1]) * (pos[1][0] - pos[0][0]) > (pos[1][1] - pos[0][1]) * (pos[2][0] - pos[0][0])


### drawing functions

def draw_triangle(pos):
    setPos(pos[0])
    startPath()
    moveTo(pos[1])
    moveTo(pos[2])
    fillPath()

def draw_wireframe_triangle(pos):
    setPos(pos[0])
    moveTo(pos[1])
    moveTo(pos[2])
    moveTo(pos[0])


### 3d drawing and geometry handling



class Ggb:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.faces = []
        
    def clear(self):
        self.vertices = []
        self.normals = []
        self.faces = []
    
    def add(self, vertices, normals, faces):
        self.faces += [[face[0] + len(self.vertices), 
                        face[1] + len(self.vertices), 
                        face[2] + len(self.vertices), 
                        face[3] + len(self.normals), 
                        face[4] + len(self.normals), 
                        face[5] + len(self.normals)] for face in faces]
                            
        self.vertices += vertices
        self.normals += normals

class Scene:
    def __init__(self):
        makeTurtle()
        
        self.ggb = Ggb()
        self.playground = getPlayground()
        self.playground.enableRepaint(False)
        
    def add_geometry(self, vertices, normals, faces):
        self.ggb.add(vertices, normals, faces)
        
    def clear_geometry(self):
        self.ggb.clear()
    
    def transform_geometry(self, tranf_mat):
        self.ggb.vertices = transform_vertices(self.ggb.vertices, tranf_mat)
    
    def poly_sort(self, poly):
        return -(self.ggb.vertices[poly[0]][2] + self.ggb.vertices[poly[1]][2] + self.ggb.vertices[poly[2]][2])    

    def present(self):
        self.playground.clear()
        
        for face in sorted(self.ggb.faces, key=self.poly_sort):
            pos = [self.ggb.vertices[face[tri]] for tri in range(0, 3)]
            
            if is_frontfacing(pos) and not(pos[0][2] <= 0 or pos[1][2] <= 0 or pos[2][2] <= 0):
                color = [n*0.5+0.5 for n in self.ggb.normals[face[3]]]
        
                
                setPenColor(color)
                setFillColor(color)
                draw_triangle(pos)
            
        self.playground.repaint()
        
### geometry

sphere_vertices = [[0.0, -1.0, 0.0], [0.723607, -0.44722, 0.525725], [-0.276388, -0.44722, 0.850649], [-0.894426, -0.447216, 0.0], [-0.276388, -0.44722, -0.850649], [0.723607, -0.44722, -0.525725], [0.276388, 0.44722, 0.850649], [-0.723607, 0.44722, 0.525725], [-0.723607, 0.44722, -0.525725], [0.276388, 0.44722, -0.850649], [0.894426, 0.447216, 0.0], [0.0, 1.0, 0.0], [-0.162456, -0.850654, 0.499995], [0.425323, -0.850654, 0.309011], [0.262869, -0.525738, 0.809012], [0.850648, -0.525736, 0.0], [0.425323, -0.850654, -0.309011], [-0.52573, -0.850652, 0.0], [-0.688189, -0.525736, 0.499997], [-0.162456, -0.850654, -0.499995], [-0.688189, -0.525736, -0.499997], [0.262869, -0.525738, -0.809012], [0.951058, 0.0, 0.309013], [0.951058, 0.0, -0.309013], [0.0, 0.0, 1.0], [0.587786, 0.0, 0.809017], [-0.951058, 0.0, 0.309013], [-0.587786, 0.0, 0.809017], [-0.587786, 0.0, -0.809017], [-0.951058, 0.0, -0.309013], [0.587786, 0.0, -0.809017], [0.0, 0.0, -1.0], [0.688189, 0.525736, 0.499997], [-0.262869, 0.525738, 0.809012], [-0.850648, 0.525736, 0.0], [-0.262869, 0.525738, -0.809012], [0.688189, 0.525736, -0.499997], [0.162456, 0.850654, 0.499995], [0.52573, 0.850652, 0.0], [-0.425323, 0.850654, 0.309011], [-0.425323, 0.850654, -0.309011], [0.162456, 0.850654, -0.499995]]
sphere_normals = [[0.1024, -0.9435, 0.3151], [0.7002, -0.6617, 0.268], [-0.268, -0.9435, 0.1947], [-0.268, -0.9435, -0.1947], [0.1024, -0.9435, -0.3151], [0.905, -0.3304, 0.268], [0.0247, -0.3304, 0.9435], [-0.8897, -0.3304, 0.3151], [-0.5746, -0.3304, -0.7488], [0.5346, -0.3304, -0.7779], [0.8026, -0.1256, 0.5831], [-0.3066, -0.1256, 0.9435], [-0.9921, -0.1256, -0.0], [-0.3066, -0.1256, -0.9435], [0.8026, -0.1256, -0.5831], [0.4089, 0.6617, 0.6284], [-0.4713, 0.6617, 0.5831], [-0.7002, 0.6617, -0.268], [0.0385, 0.6617, -0.7488], [0.724, 0.6617, -0.1947], [0.268, 0.9435, -0.1947], [0.4911, 0.7947, -0.3568], [0.4089, 0.6617, -0.6284], [-0.1024, 0.9435, -0.3151], [-0.1876, 0.7947, -0.5773], [-0.4713, 0.6617, -0.5831], [-0.3313, 0.9435, -0.0], [-0.6071, 0.7947, -0.0], [-0.7002, 0.6617, 0.268], [-0.1024, 0.9435, 0.3151], [-0.1876, 0.7947, 0.5773], [0.0385, 0.6617, 0.7488], [0.268, 0.9435, 0.1947], [0.4911, 0.7947, 0.3568], [0.724, 0.6617, 0.1947], [0.8897, 0.3304, -0.3151], [0.7947, 0.1876, -0.5773], [0.5746, 0.3304, -0.7488], [-0.0247, 0.3304, -0.9435], [-0.3035, 0.1876, -0.9342], [-0.5346, 0.3304, -0.7779], [-0.905, 0.3304, -0.268], [-0.9822, 0.1876, -0.0], [-0.905, 0.3304, 0.268], [-0.5346, 0.3304, 0.7779], [-0.3035, 0.1876, 0.9342], [-0.0247, 0.3304, 0.9435], [0.5746, 0.3304, 0.7488], [0.7947, 0.1876, 0.5773], [0.8897, 0.3304, 0.3151], [0.3066, 0.1256, -0.9435], [0.3035, -0.1876, -0.9342], [0.0247, -0.3304, -0.9435], [-0.8026, 0.1256, -0.5831], [-0.7947, -0.1876, -0.5773], [-0.8897, -0.3304, -0.3151], [-0.8026, 0.1256, 0.5831], [-0.7947, -0.1876, 0.5773], [-0.5746, -0.3304, 0.7488], [0.3066, 0.1256, 0.9435], [0.3035, -0.1876, 0.9342], [0.5346, -0.3304, 0.7779], [0.9921, 0.1256, -0.0], [0.9822, -0.1876, -0.0], [0.905, -0.3304, -0.268], [0.4713, -0.6617, -0.5831], [0.1876, -0.7947, -0.5773], [-0.0385, -0.6617, -0.7488], [-0.4089, -0.6617, -0.6284], [-0.4911, -0.7947, -0.3568], [-0.724, -0.6617, -0.1947], [-0.724, -0.6617, 0.1947], [-0.4911, -0.7947, 0.3568], [-0.4089, -0.6617, 0.6284], [0.7002, -0.6617, -0.268], [0.6071, -0.7947, -0.0], [0.3313, -0.9435, -0.0], [-0.0385, -0.6617, 0.7488], [0.1876, -0.7947, 0.5773], [0.4713, -0.6617, 0.5831]]
sphere_faces = [[0, 13, 12, 0, 0, 0], [1, 13, 15, 1, 1, 1], [0, 12, 17, 2, 2, 2], [0, 17, 19, 3, 3, 3], [0, 19, 16, 4, 4, 4], [1, 15, 22, 5, 5, 5], [2, 14, 24, 6, 6, 6], [3, 18, 26, 7, 7, 7], [4, 20, 28, 8, 8, 8], [5, 21, 30, 9, 9, 9], [1, 22, 25, 10, 10, 10], [2, 24, 27, 11, 11, 11], [3, 26, 29, 12, 12, 12], [4, 28, 31, 13, 13, 13], [5, 30, 23, 14, 14, 14], [6, 32, 37, 15, 15, 15], [7, 33, 39, 16, 16, 16], [8, 34, 40, 17, 17, 17], [9, 35, 41, 18, 18, 18], [10, 36, 38, 19, 19, 19], [38, 41, 11, 20, 20, 20], [38, 36, 41, 21, 21, 21], [36, 9, 41, 22, 22, 22], [41, 40, 11, 23, 23, 23], [41, 35, 40, 24, 24, 24], [35, 8, 40, 25, 25, 25], [40, 39, 11, 26, 26, 26], [40, 34, 39, 27, 27, 27], [34, 7, 39, 28, 28, 28], [39, 37, 11, 29, 29, 29], [39, 33, 37, 30, 30, 30], [33, 6, 37, 31, 31, 31], [37, 38, 11, 32, 32, 32], [37, 32, 38, 33, 33, 33], [32, 10, 38, 34, 34, 34], [23, 36, 10, 35, 35, 35], [23, 30, 36, 36, 36, 36], [30, 9, 36, 37, 37, 37], [31, 35, 9, 38, 38, 38], [31, 28, 35, 39, 39, 39], [28, 8, 35, 40, 40, 40], [29, 34, 8, 41, 41, 41], [29, 26, 34, 42, 42, 42], [26, 7, 34, 43, 43, 43], [27, 33, 7, 44, 44, 44], [27, 24, 33, 45, 45, 45], [24, 6, 33, 46, 46, 46], [25, 32, 6, 47, 47, 47], [25, 22, 32, 48, 48, 48], [22, 10, 32, 49, 49, 49], [30, 31, 9, 50, 50, 50], [30, 21, 31, 51, 51, 51], [21, 4, 31, 52, 52, 52], [28, 29, 8, 53, 53, 53], [28, 20, 29, 54, 54, 54], [20, 3, 29, 55, 55, 55], [26, 27, 7, 56, 56, 56], [26, 18, 27, 57, 57, 57], [18, 2, 27, 58, 58, 58], [24, 25, 6, 59, 59, 59], [24, 14, 25, 60, 60, 60], [14, 1, 25, 61, 61, 61], [22, 23, 10, 62, 62, 62], [22, 15, 23, 63, 63, 63], [15, 5, 23, 64, 64, 64], [16, 21, 5, 65, 65, 65], [16, 19, 21, 66, 66, 66], [19, 4, 21, 67, 67, 67], [19, 20, 4, 68, 68, 68], [19, 17, 20, 69, 69, 69], [17, 3, 20, 70, 70, 70], [17, 18, 3, 71, 71, 71], [17, 12, 18, 72, 72, 72], [12, 2, 18, 73, 73, 73], [15, 16, 5, 74, 74, 74], [15, 13, 16, 75, 75, 75], [13, 0, 16, 76, 76, 76], [12, 14, 2, 77, 77, 77], [12, 13, 14, 78, 78, 78], [13, 1, 14, 79, 79, 79]]


### mainloop

scene = Scene()

projection_matrix = perspective_matrix(1, radians(110), 0.01, 100, 1000)


while True:
    scene.clear_geometry()
    t = time()
    
    
    for x in range(-2, 2):
        for y in range(-2, 2):
            for z in range(-1, 1):
                scene.add_geometry(transform_vertices(sphere_vertices, matrix_multiply(translation_matrix([x * 3 + 1.5, y * 3 + 1.5, z * 3 + 1.5]), rotation_matrix_y(t+x+y+z))), sphere_normals, sphere_faces)
    
    

    scene.transform_geometry(matrix_multiply(matrix_multiply(matrix_multiply(projection_matrix, translation_matrix([0, 0, -25])), rotation_matrix_x(0.3)), rotation_matrix_y(t / 3)))

    scene.present()
