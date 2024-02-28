# Importando os módulos necessários
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import graficos  # Supondo que "graficos" seja um módulo personalizado contendo funções de renderização

# Definição da classe Dado
class Dado(object):
    # Inicialização da classe
    tecla_esquerda = False
    tecla_direita = False
    tecla_cima = False
    tecla_baixo = False
    angulo = 0
    angulo_cubo = 0
    def __init__(self):
        # Inicialização de variáveis e carregamento de texturas e modelos
        self.vertices = []
        self.faces = []
        self.rubik_id = graficos.carregar_textura("dado.png")  # Carrega a textura do cubo
        self.surface_id = graficos.carregar_textura("textura.png")  # Carrega a textura da superfície
        self.coordenadas = [15, 0, 0]  # Coordenadas iniciais da câmera
        self.terreno = graficos.CarregadorObjeto("plano.txt")  # Carrega o modelo do plano
        self.piramide = graficos.CarregadorObjeto("cena.txt")  # Carrega o modelo da pirâmide
        self.dado = graficos.CarregadorObjeto("dado.txt")  # Carrega o modelo do cubo

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
        glRotatef(self.angulo_cubo, 0, 1, 0)
        glRotatef(45, 0, 0, 1)
        self.dado.renderizar_dado(self.rubik_id, ((0, 0), (1, 0), (1, 1), (0, 1)))  # Renderiza o cubo

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
        # Atualizações de movimento da câmera e do cubo
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
            self.girar(-1.2)
        elif pos[0] > 565:
            self.girar(1.2)
        
        if self.angulo_cubo >= 360:
            self.angulo_cubo = 0
        else:
            self.angulo_cubo += 0.5
    
    def liberar_tecla(self):
        # Função chamada quando uma tecla é liberada
        self.tecla_esquerda = False
        self.tecla_direita = False
        self.tecla_cima = False
        self.tecla_baixo = False
    
    def deletar_textura(self):
        # Função para deletar as texturas carregadas
        glDeleteTextures(self.rubik_id)
        glDeleteTextures(self.surface_id)

# Função principal do programa
def principal():
    pygame.init()
    pygame.display.set_mode((1024, 768), pygame.DOUBLEBUF | pygame.OPENGL)  # Inicializa a janela Pygame
    pygame.display.set_caption("PyOpenGL 3D")
    relogio = pygame.time.Clock()
    feito = False
    
    # Configuração da matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 640.0 / 480.0, 0.1, 200.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    # Instanciação do objeto Dado
    dado = Dado()
    
    # Loop principal do jogo
    while not feito:
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT: 
                feito = True 
            if evento.type == pygame.KEYDOWN:
                # Eventos de pressionamento de tecla
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    dado.mover_esquerda()
                    dado.tecla_esquerda = True
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    dado.mover_direita()
                    dado.tecla_direita = True
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    dado.mover_frente()
                    dado.tecla_cima = True
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    dado.mover_trás()
                    dado.tecla_baixo = True
            if evento.type == pygame.KEYUP:
                # Eventos de liberação de tecla
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    dado.liberar_tecla()
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    dado.liberar_tecla()
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    dado.liberar_tecla()
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    dado.liberar_tecla()
        
        dado.atualizar()
        dado.renderizar_cena()
        
        pygame.display.flip()
        relogio.tick(30)
    
    dado.deletar_textura()
    pygame.quit()

if __name__ == '__main__':
    principal()
