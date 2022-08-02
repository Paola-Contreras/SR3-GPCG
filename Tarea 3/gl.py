#Universidad del Valle de Guatemala 
#Gráficos por computador 
#Gabriela Paola Contreras Guerra 20213
#SR3 - OBJ objects 

#Imports 
import struct
from obj import Obj
import math_lib as m
import random as rand 
from collections import namedtuple

#Vectors - It just make code more redable 
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


#SPACES THAT I WANT TO USE 
def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

# function to set colors 
def color(r, g, b):
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)] )


class Renderer(object):

    # Define size of the screen 
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.clearColor = color(0,0,0)
        self.currColor = color(1,1,1)
        self.glViewport(0,0,self.width, self.height)
        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    #Determinate the background color & array of pixels
    def glClear(self):
        self.pixels = [[ self.clearColor 
                        for y in range(self.height)] # por cada y en el ancho se le agrega el color definido 
                        for x in range(self.width)] # por cada x en el largo se le agrega el color definido

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)

     # HOW TO MAKE POINTS 
    def glPoint(self, x, y, clr = None): 
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    #HOW TO MAKE LINES 
    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0,clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Inclinacion de una linea 
        steep = dy > dx

        #Invierto las lineas (Dibujo vertical y no horizontal)
        #Slope is bigger than 1 so I change it 
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        #Draw left to right 
        #Initial dot is bigger than final dot I change the values      
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        #Need to redifine because I change the invert the values 
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5 #Represents the middle of a pixel # Este puede cambiar de acuerdo a nuestras necesidades, pero se recomienda usar .5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            #Draw de manera vertical
            if steep:
                self.glPoint(y, x, clr)

            #Draw de manera horizontal 
            else:
                self.glPoint(x, y, clr)

            offset += m

            if offset >= limit:
                if y0 < y1: #I am going down to up (well the line)
                    y += 1
                else: # The line is been drawing up to down
                    y -= 1
                
                limit += 1

    #Function to create matrix 
    def glCreateObjectMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):

        #Data of the matrix 
        TM = [1, 0, 0, translate.x, 0, 1, 0, translate.y, 0, 0, 1, translate.z, 0, 0, 0, 1]
        SM = [scale.x, 0, 0, 0, 0, scale.y, 0, 0, 0, 0, scale.z, 0, 0, 0, 0, 1]
        RM = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]

        #Create Matrix 
        translation = m.createMatrix(4,4, TM)
        scales = m.createMatrix(4,4, SM)
        rotation = m.createMatrix(4,4,RM)

        #Multiplication of matrix 
        Matrix_init = m.multiplyMatrix(translation, rotation)
        Matrix_final = m.multiplyMatrix(Matrix_init, scales)

        return Matrix_final

    def glTransform(self, vertex, matrix):
        
        #Vector 
        v = (vertex[0], vertex[1], vertex[2], 1)
        
        #Multiplication of matrix and vector 
        vt = m.matmulvec(matrix, v)

        vf = V3(vt[0] / vt[3],
                vt[1] / vt[3],
                vt[2] / vt[3])

        return vf


    #GENERATE OBJ 
    def glLoadModel(self, filename, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):
        #Open file 
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]

            v0 = self.glTransform(v0, modelMatrix)
            v1 = self.glTransform(v1, modelMatrix)
            v2 = self.glTransform(v2, modelMatrix)


            #COLOR OBS 
            self.glTriangle_std(v0, v1, v2, color(rand.random(),
                                                  rand.random(),
                                                  rand.random()))

    #Fill a poligon base on triagles 
    def glTriangle_std(self, A, B, C, clr = None):
        
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        self.glLine(A,B, clr)
        self.glLine(B,C, clr)
        self.glLine(C,A, clr)

        def flatBottom(vA,vB,vC):
            try:
                mBA = (vB.x - vA.x) / (vB.y - vA.y)
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
            except:
                pass
            else:
                x0 = vB.x
                x1 = vC.x
                for y in range(int(vB.y), int(vA.y)):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA,vB,vC):
            try:
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
                mCB = (vC.x - vB.x) / (vC.y - vB.y)
            except:
                pass
            else:
                x0 = vA.x
                x1 = vB.x
                for y in range(int(vA.y), int(vC.y), -1):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 -= mCA
                    x1 -= mCB

        if B.y == C.y:
            # Flat bottom 
            flatBottom(A,B,C)
        elif A.y == B.y:
            # Flat top
            flatTop(A,B,C)
        else:
            # Two types of triagnles. I use the intercept teorem 
            D = V2( A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottom(A,B,D)
            flatTop(B,D,C)

    #Function to define image 
    def glFinish(self, filename):
        with open(filename, "wb") as file:
             #HEADER (STEP 1) default BM size(14 bytes)
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))

            #offset 40 bytes + header 14 bytes and color w * h * 3(de bytes)
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

           #INFO HEADER (SETP 2) size(40 bytes)
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))

             #Entre mas color quiera debo de aumentar el bits per pixel 
            file.write(word(24))
            file.write(dword(0)) #compression
            file.write(dword(self.width * self.height * 3)) #size of the screen
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #COLOR TABLE 
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
