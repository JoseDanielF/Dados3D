# Módulos
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import graficos 

# Definição da classe Bloco
class Bloco(object):
    # Inicialização da classe
    tecla_esquerda = False
    tecla_direita = False
    tecla_cima = False
    tecla_baixo = False
    angulo = 0
    angulo_bloco = 0
    def __init__(self, textura, coordenadas):
        # Inicialização de variáveis e carregamento de texturas e modelos
        self.vertices = []
        self.faces = []
        self.rubik_id = graficos.carregar_textura(textura)  # Carrega a textura do cubo
        self.surface_id = graficos.carregar_textura("grama.png")  # Carrega a textura da superfície
        self.coordenadas = coordenadas  # Coordenadas iniciais da câmera
        self.terreno = graficos.CarregadorObjeto("plano.txt")  # Carrega o modelo do plano
        self.piramide = graficos.CarregadorObjeto("cena.txt")  # Carrega o modelo da pirâmide
        self.bloco = graficos.CarregadorObjeto("bloco.txt")  # Carrega o modelo do cubo

    # Renderização da cena
    def renderizar_cena(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Configuração das luzes
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [2, 2, 2, 1])
        glLightfv(GL_LIGHT0, GL_POSITION, [4, 8, 1, 1])
        
        glTranslatef(0, -0.5, 0)  # Translação da cena

        # Configuração da câmera
        gluLookAt(0, 0, 0, math.sin(math.radians(self.angulo)), 0, math.cos(math.radians(self.angulo)) * -1, 0, 1, 0)
        
        glTranslatef(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2])  # Translação da câmera

        # Renderização dos objetos
        self.terreno.renderizar_textura(self.surface_id, ((0, 0), (2, 0), (2, 2), (0, 2)))  # Renderiza o plano
        self.piramide.renderizar_cena()  # Renderiza a pirâmide
        
        # Translação e rotação do cubo
        glTranslatef(0, 2, 0)
        glRotatef(self.angulo_bloco, 0, 1, 0)
        glRotatef(45, 0, 0, 1)
        self.bloco.renderizar_dado(self.rubik_id, ((0, 0), (1, 0), (1, 1), (0, 1)))  # Renderiza o cubo

    # Métodos para movimentação da câmera e do cubo
    def mover_frente(self):
        self.coordenadas[2] += 0.1 * math.cos(math.radians(self.angulo))
        self.coordenadas[0] -= 0.1 * math.sin(math.radians(self.angulo))
        
    def mover_trás(self):
        self.coordenadas[2] -= 0.1 * math.cos(math.radians(self.angulo))
        self.coordenadas[0] += 0.1 * math.sin(math.radians(self.angulo))
            
    def mover_esquerda(self):
        self.coordenadas[0] += 0.1 * math.cos(math.radians(self.angulo))
        self.coordenadas[2] += 0.1 * math.sin(math.radians(self.angulo))
        
    def mover_direita(self):
        self.coordenadas[0] -= 0.1 * math.cos(math.radians(self.angulo))
        self.coordenadas[2] -= 0.1 * math.sin(math.radians(self.angulo))
        
    def girar(self, n):
        if self.angulo >= 360 or self.angulo <= -360:
            self.angulo = 0
        self.angulo += n
            
    def atualizar(self):
        # Atualizações de movimento da câmera e do bloco
        if self.tecla_esquerda:
            self.mover_esquerda()
        elif self.tecla_direita:
            self.mover_direita()
        elif self.tecla_cima:
            self.mover_frente()
        elif self.tecla_baixo:
            self.mover_trás()
            
        pos = pygame.mouse.get_pos()
        if pos[0] < 75:
            self.girar(-0.5)  # Reduzindo a velocidade de rotação
        elif pos[0] > 565:
            self.girar(0.5)  # Reduzindo a velocidade de rotação
        
        if self.angulo_bloco >= 360:
            self.angulo_bloco = 0
        else:
            self.angulo_bloco += 0.2  # Reduzindo a velocidade de rotação
    
    def liberar_tecla(self):
        # Função chamada quando uma tecla é liberada
        self.tecla_esquerda = False
        self.tecla_direita = False
        self.tecla_cima = False
        self.tecla_baixo = False
    
    def deletar_textura(self):
        # Deleta a textura do cubo
        glDeleteTextures(1, (GLuint * 1)(self.rubik_id))
        # Deleta a textura da superfície
        glDeleteTextures(1, (GLuint * 1)(self.surface_id))

# Função principal do programa
def principal():
    pygame.init()
    largura_janela = 1024
    altura_janela = 768
    pygame.display.set_mode((largura_janela, altura_janela), pygame.DOUBLEBUF | pygame.OPENGL)  # Inicializa a janela Pygame
    pygame.display.set_caption("PyOpenGL 3D")
    relogio = pygame.time.Clock()
    encerrado = False
    
    # Configuração da matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, largura_janela / altura_janela, 0.1, 200.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    
    bloco1 = Bloco("minecraft_bloco.png", [-5, 0, 0])

    # Loop principal do jogo
    while not encerrado:
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT: 
                encerrado = True 
            if evento.type == pygame.KEYDOWN:
                # Eventos de pressionamento de tecla
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    bloco1.mover_esquerda()
                    bloco1.tecla_esquerda = True
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    bloco1.mover_direita()
                    bloco1.tecla_direita = True
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    bloco1.mover_frente()
                    bloco1.tecla_cima = True
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    bloco1.mover_trás()
                    bloco1.tecla_baixo = True
            if evento.type == pygame.KEYUP:
                # Eventos de liberação de tecla
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    bloco1.liberar_tecla()
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    bloco1.liberar_tecla()
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    bloco1.liberar_tecla()
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    bloco1.liberar_tecla()
        
        bloco1.atualizar()
        bloco1.renderizar_cena()
        relogio.tick(60)
        pygame.display.flip()
    
    bloco1.deletar_textura()
    pygame.quit()

if __name__ == '__main__':
    principal()
