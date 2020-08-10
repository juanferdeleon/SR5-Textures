'''
        SR3 Obj Models

Creado por:

    Juan Fernando De Leon Quezada   Carne 17822

- Bitmap Class

'''

import struct
import collections
from obj import ObjReader

def char(c):
    '''1 Byte'''

    return struct.pack('=c', c.encode('ascii'))

def word(w):
    '''2 Bytes'''

    return struct.pack('=h', w)

def dword(d):
    '''4 Bytes'''

    return struct.pack('=l', d)

def color(r,g,b):
    '''Set pixel color'''

    return bytes([b, g, r])

#Constants
V2 = collections.namedtuple('Vertex2', ['x', 'y'])
V3 = collections.namedtuple('Vertex3', ['x', 'y', 'z'])

#Arithmetics

def sum(v0, v1):
    '''Vector Sum'''
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
    '''Vector Substraction'''
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
    '''Vector Multiplication'''
    return V3(v0.x * k, v0.y * k, v0.z * k)

def dot(v0, v1):
    '''Dot Product'''
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
    '''Cross Product'''
    
    x = v0.y * v1.z - v0.z * v1.y
    y = v0.z * v1.x - v0.x * v1.z
    z = v0.x * v1.y - v0.y * v1.x

    return V3(x, y, z)

def magnitud(v0):
    '''Vector Magnitud'''
    return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
    '''Normal vector'''
    l = magnitud(v0)
    if l == 0:
        return V3(0, 0, 0)
    else:
        return V3(v0.x/l, v0.y/l, v0.z/l)

def bbox(A, B, C):
    
    xs = sorted([int(A.x), int(B.x), int(C.x)])
    ys = sorted([int(A.y), int(B.y), int(C.y)])
    a = V2(int(xs[0]), int(ys[0]))
    b = V2(int(xs[2]), int(ys[2]))    
    
    return a, b

def barycentric(A, B, C, P):
    '''Convert vertices to barycentric coordinates'''
    
    cx, cy, cz = cross(V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y))

    #CZ Cannot be less 1
    if cz == 0:
        return -1, -1, -1

    #Calculate the barycentric coordinates
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    return  w, v, u

class Bitmap(object):
    '''Bitmap Class'''

    def __init__(self, height, width):
        '''Constructor'''

        self.height = height
        self.width = width
        self.framebuffer = []
        self.zbuffer = []
        self.clear_color = color(0, 0, 0)
        self.vertex_color = color(255, 0, 0)
        self.glClear()

    def glInit(self):
        '''Initialize any internal objects that your renderer software requires'''

        pass

    def glCreateWindow(self, height, width):
        '''Initialize framebuffer, img will be this size'''

        self.height = height
        self.width = width
        self.glClear()
    
    def glViewPort(self, x, y, width, height):
        '''Define the area of the image to draw on'''

        self.x = x
        self.y = y
        self.vpx = width
        self.vpy = height

    def glClear(self):
        '''Set all pixels to same color'''

        self.framebuffer = [
            [self.clear_color for x in range(self.width)] for y in range(self.height)
        ]

        self.zbuffer = [
            [-1*float('inf') for x in range(self.width)] for y in range(self.height)
            ]
    
    def glClearColor(self, r, g, b):
        '''Can change the color of glClear(), parameters must be numbers in the 
        range of 0 to 1.'''

        try:
            self.rc = round(255*r)
            self.gc = round(255*g)
            self.bc = round(255*b)
            self.clear_color = color(self.rc, self.rg, self.rb)
        except ValueError:
            print('\nERROR: Please enter a number between 1 and 0\n')
    
    def glVertex(self, x, y):
        '''Change the color of a point on the screen. The x, y coordinates are 
        specific to the viewport that they defined with glViewPort().'''

        if x <= 1 and x>= -1 and y >= -1 and y <= 1:
                
                if x > 0:
                        self.vx = self.x + round(round(self.vpx/2)*x) - 1
                if y > 0:
                        self.vy = self.y + round(round(self.vpy/2)*y) - 1
                if x <= 0:
                        self.vx = self.x + round(round(self.vpx/2)*x)
                if y <= 0:
                        self.vy = self.y + round(round(self.vpy/2)*y)
                
                self.glPoint(self.vx,self.vy, self.vertex_color)
        else:
                pass
    
    def glColor(self, r, g, b):
        '''Change the color glVertex() works with. The parameters must 
        be numbers in the range of 0 to 1.'''

        try:
            self.rv = round(255*r)
            self.gv = round(255*g)
            self.bv = round(255*b)
            self.vertex_color = color(self.rv,self.gv,self.bv)
        except ValueError:
                print('\nERROR: Please enter a number between 1 and 0\n')

    def glPoint(self, x, y, color):
        '''Draw a point'''
        x = int(round((x+1) * self.width / 2))
        y = int(round((y+1) * self.height / 2))
        try:
                self.framebuffer[y][x] = color
        except IndexError:
                print("\nPixel is outside the limits of the image\n")
    
    def glLine(self, x0, y0, x1, y1):
        '''Draw a straight line through the succession of pixels'''

        #Convert the values between -1 and 1 to DMC coordenates
        x0 = int(round((x0 + 1) * self.width / 2))
        y0 = int(round((y0 + 1) * self.height / 2))
        x1 = int(round((x1 + 1) * self.width / 2))
        y1 = int(round((y1 + 1) * self.height / 2))

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx
        
        #If dy is greater than dx then we exchange each of the coordinates
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        #If the starting point in x is greater than the final point then we exchange the points
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Determine the points that will form the line
        offset = 0.5 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0

        #Fill the line with points without leaving space between
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint((float(y)/(float(self.width)/2))-1,(float(x)/(float(self.height)/2))-1,self.vertex_color)
            else:
                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)
            offset += dy

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * dx

    def glTransform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
        '''Transforms vertex into tuple'''
        try:
            return V3(
                (int(round((vertex[0]+1) * self.width / 2)) + translate[0]) * scale[0],
                (int(round((vertex[1]+1) * self.height / 2)) + translate[1]) * scale[1],
                (int(round((vertex[2]+1) * self.width / 2)) + translate[2]) * scale[2]
            )
        except IndexError:
            return V3(
                (int(round((vertex[0]+1) * self.width / 2)) + translate[0]) * scale[0],
                (int(round((vertex[1]+1) * self.height / 2)) + translate[1]) * scale[1],
                (int(round((0.0+1) * self.width / 2)) + translate[2]) * scale[2]
            )

    def glFillTriangle(self, a, b, c):
        '''Algorithm for filling triangles'''

        if a.y > b.y:
            a, b = b, a
        if a.y > c.y:
            a, c = c, a
        if b.y > c.y:
            b, c = c, b
        
        ac_x_slope = c.x - a.x
        ac_y_slope = c.y - a.y

        if ac_y_slope == 0:
            return
        
        inverse_ac_slope = ac_x_slope / ac_y_slope

        ab_x_slope = b.x - a.x
        ab_y_slope = b.y - a.y

        if ab_y_slope != 0:

            inverse_ab_slope = ab_x_slope / ab_y_slope

            for y in range(a.y, b.y + 1):
                x0 = round(a.x - inverse_ac_slope * (a.y - y))
                xf = round(a.x - inverse_ab_slope * (a.y - y))

                if x0 > xf:
                    x0, xf = xf, x0
                
                for x in range(x0, xf + 1):
                    self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)
        
        bc_x_slope = c.x - b.x
        bc_y_slope = c.y - b.y

        if bc_y_slope:

            inverse_bc_slope = bc_x_slope / bc_y_slope

            for y in range (b.y, c.y + 1):
                x0 = round(a.x - inverse_ac_slope * (a.y - y))
                xf = round(b.x - inverse_bc_slope * (b.y - y))

                if x0 > xf:
                    x0, xf = xf, x0
                
                for x in range(x0, xf + 1):
                    self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)
                    
    def triangle(self, A, B, C, color=None, texture=None, tex_coords=(), intensity = 1):
        '''Algorithm for filling triangles with barycentric coords'''

        bbox_min, bbox_max = bbox(A, B, C)

        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y +1):

                w, v, u = barycentric(A, B, C, V2(x, y))

                if w < 0 or v < 0 or u < 0:
                    continue

                if texture:
                    ta, tb, tc = tex_coords
                    tx = ta.x * w + tb.x * v + tc.x * u
                    ty = ta.y * w + tb.y * v + tc.y * u
                    
                    color = texture.get_color(tx, ty, intensity)
                    self.vertex_color = color

                z = A.z * w + B.z * v + C.z * u

                if z > self.zbuffer[y][x]:
                    self.glPoint((float(x)/(float(self.width)/2))-1, (float(y)/(float(self.height)/2))-1,self.vertex_color)
                    self.zbuffer[y][x] = z

    def glFillPolygon(self, polygon):
        '''Fill any given polygon'''
        #Based on Point-in-Polygon (PIP) Algorithm
        for y in range(self.height):
            for x in range(self.width):
                i = 0
                j = len(polygon) - 1
                draw_point = False
                #Verifies if point is in between the boundaries
                for i in range(len(polygon)):
                    if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
                        if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                            draw_point = not draw_point
                    j = i
                if draw_point:
                    self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)

    def glLoadObjModel(self, file_name, texture=None, translate=(0,0, 0), scale=(1,1, 1)):
        '''Load and Render .obj file'''
        #Reads .obj file
        model = ObjReader(file_name)
        model.readLines()

        light = V3(0, 0.4, 1)
        
        for face in model.faces:
            vertices_ctr = len(face)

            if vertices_ctr == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                
                a = self.glTransform(model.vertices[f1], translate, scale)
                b = self.glTransform(model.vertices[f2], translate, scale)
                c = self.glTransform(model.vertices[f3], translate, scale)

                normal = norm(cross(sub(b,a),sub(c,a)))

                light = norm(light)

                intensity = dot(normal, light)

                if intensity < 0:
                    continue
                
                if texture:
                    tv1 = face[0][1] - 1
                    tv2 = face[1][1] - 1
                    tv3 = face[2][1] - 1
                    
                    tvA = self.glTransform(model.tex_coords[tv1],translate,scale)
                    tvB = self.glTransform(model.tex_coords[tv2],translate,scale)
                    tvC = self.glTransform(model.tex_coords[tv3],translate,scale)

                    self.triangle(a,b,c, texture = texture, tex_coords = (tvA, tvB, tvC), intensity = intensity)
                
                else:
                    self.triangle(a,b,c, color = self.glColor(intensity, intensity, intensity))
    
    def glWrite(self, file_name):
        '''Write Bitmap File'''
        
        bmp_file = open(file_name, 'wb')

        #File header 14 bytes
        bmp_file.write(char('B'))
        bmp_file.write(char('M'))
        bmp_file.write(dword(14 + 40 + self.width * self.height))
        bmp_file.write(dword(0))
        bmp_file.write(dword(14 + 40))
        
        #File info 40 bytes
        bmp_file.write(dword(40))
        bmp_file.write(dword(self.width))
        bmp_file.write(dword(self.height))
        bmp_file.write(word(1))
        bmp_file.write(word(24))
        bmp_file.write(dword(0))
        bmp_file.write(dword(self.width * self.height * 3))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))
        bmp_file.write(dword(0))

        # Pixeles, 3 bytes each
        for x in range(self.height):
            for y in range(self.width):
                self.framebuffer[x][y]
                bmp_file.write(self.framebuffer[x][y])
            
        bmp_file.close()