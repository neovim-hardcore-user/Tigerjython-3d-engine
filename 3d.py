### general import stuff

from gturtle import *
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

sphere_vertices = [[0.0, -0.749711, -1.0], [0.866025, -0.749711, 0.5], [-0.866025, -0.749711, 0.5], [0.0, 0.749711, 0.0]]
sphere_normals = [[0.8216, 0.3163, -0.4743], [-0.0, -1.0, -0.0], [-0.0, 0.3163, 0.9486], [-0.8216, 0.3163, -0.4743]]
sphere_faces = [[0, 3, 1, 0, 0, 0], [0, 1, 2, 1, 1, 1], [1, 3, 2, 2, 2, 2], [2, 3, 0, 3, 3, 3]]


### mainloop

scene = Scene()

projection_matrix = perspective_matrix(1, radians(110), 0.01, 100, 1000)


while True:
    scene.clear_geometry()
    t = time()
    
    
    for x in range(-3, 3):
        for y in range(-3, 3):
            for z in range(-3, 3):
                scene.add_geometry(transform_vertices(sphere_vertices, matrix_multiply(translation_matrix([x * 3 + 1.5, y * 3 + 1.5, z * 3 + 1.5]), rotation_matrix_y(t+x+y+z))), sphere_normals, sphere_faces)
    
    

    scene.transform_geometry(matrix_multiply(matrix_multiply(matrix_multiply(projection_matrix, translation_matrix([0, 0, -25])), rotation_matrix_x(0.3)), rotation_matrix_y(t)))

    scene.present()