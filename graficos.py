import pygame
from OpenGL.GL import *

def carregar_textura(filename):
    textureSurface = pygame.image.load(filename)
    textureData = pygame.image.tostring(textureSurface,"RGBA",1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,ID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
    return ID

class CarregadorObjeto(object):
    def __init__(self,filename):
        self.vertices = []
        self.quad_faces = []
        self.normals = []
        #-----------------------
        try:
            f = open(filename)
            n = 1
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") +1 
                    index2 = line.find(" ",index1+1)  
                    index3 = line.find(" ",index2+1) 
                        
                    vertex = (float(line[index1:index2]),float(line[index2:index3]),float(line[index3:-1]))
                    vertex = (round(vertex[0],2),round(vertex[1],2),round(vertex[2],2))
                    self.vertices.append(vertex)
                    
                elif line[:2] == "vn":
                    index1 = line.find(" ") +1 
                    index2 = line.find(" ",index1+1)  
                    index3 = line.find(" ",index2+1)
                    
                    normal = (float(line[index1:index2]),float(line[index2:index3]),float(line[index3:-1]))
                    normal = (round(normal[0],2),round(normal[1],2),round(normal[2],2)) 
                    self.normals.append(normal)
                    
                elif line[0] == "f":
                    string = line.replace("//","/")
                    #---------------------------------------------------
                    i = string.find(" ")+1
                    face  = []
                    for item in range(string.count(" ")):
                        if string.find(" ",i) == -1:
                            face.append(string[i:-1])
                            break
                        face.append(string[i:string.find(" ",i)])
                        i = string.find(" ",i) +1
                    #---------------------------------------------------
            self.quad_faces.append(tuple(face))
                   
            f.close()
        except IOError:
            print("Não foi possível abrir o arquivo: ",filename)
            
    def renderizar_cena(self):    
        if len(self.quad_faces) > 0:
            #----------------------------------
            glBegin(GL_QUADS)
            for face in (self.quad_faces):
                n = face[0]
                normal = self.normals[int(n[n.find("/")+1:])-1] 
                glNormal3fv(normal)
                for f in (face):
                    glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
            glEnd()
            #-----------------------------------
       
    def renderizar_textura(self,textureID,texcoord):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,textureID)
        
        glBegin(GL_QUADS)
        for face in self.quad_faces:
            n = face[0]
            normal = self.normals[int(n[n.find("/")+1:])-1] 
            glNormal3fv(normal)
            for i,f in enumerate(face):
                glTexCoord2fv(texcoord[i])
                glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
        glEnd()
    
        glDisable(GL_TEXTURE_2D)
       
    def renderizar_dado(self,textureID,texcoord):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,textureID)
        glBegin(GL_POLYGON); 
        glTexCoord2f(0.250,0.500); glVertex3f(-1.00, 1.00, 1.00);
        glTexCoord2f(0.250,0.250); glVertex3f(-1.00,-1.00, 1.00);
        glTexCoord2f(0.500,0.250); glVertex3f( 1.00,-1.00, 1.00);
        glTexCoord2f(0.500,0.500); glVertex3f( 1.00, 1.00, 1.00);
        glEnd();
        glBegin(GL_POLYGON); 
        glTexCoord2f(0.000,0.500); glVertex3f(-1.00, 1.00,-1.00);
        glTexCoord2f(0.000,0.250); glVertex3f(-1.00,-1.00,-1.00);
        glTexCoord2f(0.250,0.250); glVertex3f(-1.00,-1.00, 1.00);
        glTexCoord2f(0.250,0.500); glVertex3f(-1.00, 1.00, 1.00);
        glEnd();
        glBegin(GL_POLYGON); 
        glTexCoord2f(0.500,0.500); glVertex3f( 1.00, 1.00, 1.00);
        glTexCoord2f(0.500,0.250); glVertex3f( 1.00,-1.00, 1.00);
        glTexCoord2f(0.750,0.250); glVertex3f( 1.00,-1.00,-1.00);
        glTexCoord2f(0.750,0.500); glVertex3f( 1.00, 1.00,-1.00);
        glEnd();
        glBegin(GL_POLYGON); 
        glTexCoord2f(0.250,0.750); glVertex3f(-1.00, 1.00,-1.00);
        glTexCoord2f(0.250,0.500); glVertex3f(-1.00, 1.00, 1.00);
        glTexCoord2f(0.500,0.500); glVertex3f( 1.00, 1.00, 1.00);
        glTexCoord2f(0.500,0.750); glVertex3f( 1.00, 1.00,-1.00);
        glEnd();
        glBegin(GL_POLYGON); 
        glTexCoord2f(0.250,0.250); glVertex3f(-1.00, -1.00, 1.00);
        glTexCoord2f(0.250,0.000); glVertex3f(-1.00, -1.00,-1.00);
        glTexCoord2f(0.500,0.000); glVertex3f( 1.00, -1.00,-1.00);
        glTexCoord2f(0.500,0.250); glVertex3f( 1.00, -1.00, 1.00);
        glEnd();
        glBegin(GL_POLYGON); 
        glTexCoord2f(0.750,0.500); glVertex3f( 1.00, 1.00,-1.00);
        glTexCoord2f(0.750,0.250); glVertex3f( 1.00,-1.00,-1.00);
        glTexCoord2f(1.000,0.250); glVertex3f(-1.00,-1.00,-1.00);
        glTexCoord2f(1.000,0.500); glVertex3f(-1.00, 1.00,-1.00);
        glEnd();
        glDisable(GL_TEXTURE_2D);

        
    
