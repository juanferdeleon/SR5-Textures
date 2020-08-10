'''
        SR3 Obj Models

Creado por:

    Juan Fernando De Leon Quezada   Carne 17822

Engine 3D

'''

from gl import Bitmap

bmp = Bitmap(1000, 1000)

def glInit():
    return bmp


if __name__ == '__main__':
    '''Main Program'''

    #Initialize bmp Object
    bmp = glInit()

    #Set all pixels to same color
    bmp.glClear()

    #Set pixel Colors
    bmp.glColor(1, 1, 1)

    bmp.glLoadObjModel('face.obj')
    
    #Output BMP
    bmp.glWrite("test.bmp")
