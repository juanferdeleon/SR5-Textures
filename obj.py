'''
        SR3 Obj Models

Creado por:

    Juan Fernando De Leon Quezada   Carne 17822

- Obj File Reader Class

'''

class ObjReader(object):
    '''Obj File Reader'''
    
    def __init__(self, filename):
        '''Constructor'''
        #Open and read .obj file
        with open(filename) as obj_file:
            self.lines = obj_file.read().splitlines()
        
        self.vertices = []
        self.normals = []
        self.tex_coords = []
        self.faces = []

        #Reads individual lines from .obj file
        self.readLines()
    

    def removeSpaces(self, face):
        '''Remove empty spaces if they exist'''

        store_data = face.split('/')

        if ("") in store_data:
            store_data.remove("")
        
        return map(int, store_data)

    def readLines(self):
        '''Read individual lines from .obj file'''
        
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float,value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float,value.split(' '))))
                elif prefix == 'vt':
                    self.tex_coords.append(list(map(float,value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(self.removeSpaces(face)) for face in value.split(' ')])