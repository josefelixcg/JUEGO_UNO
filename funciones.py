import pygame as pyg
import os

pyg.font.init()

heightq, widthq = 800, 600
screen = pyg.display.set_mode((heightq, widthq), pyg.RESIZABLE)

def size_imgen(background_original, screen):
    ventana= screen.get_size()
    return pyg.transform.scale(background_original, ventana)

#COLORES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#FUENTES
# Fuentes
font_large = pyg.font.SysFont('Arial', 36)
font_medium = pyg.font.SysFont('Arial', 24)
font_small = pyg.font.SysFont('Arial', 18)

class User:
    def __init__(self, nombre, vida, color):
        self.nombre = nombre
        self.vida_max = vida
        self.vida_actual = vida
        self.color = color
        self.ataques = []
        self.especiales = 3 #el número de ataques especiales
        
    def attack(self, tipo_ataque, oponente):
        if tipo_ataque == "NORMAL":
            destruye = 10
            oponente.vida_actual -= destruye
            return f"{self.nombre} usa ataque normal! (-{destruye} vidas)"
        elif tipo_ataque == "ESPECIAL" and self.especiales > 0:
            destruye = 20
            oponente.vida_actual -= destruye
            self.especiales -= 1
            return f"{self.nombre} usa ataque normal! (-{destruye} vidas)"
        else:
            return "Ataque especial no disponible o inválido"
    
    def posicionamiento(self, x, y):
        pyg.draw.rect(screen, YELLOW, (x, y, 200, 30), 2)
        vida_width = int(200 * (self.vida_actual / self.vida_max))
        pyg.draw.rect(screen, self.color, (x, y, vida_width, 30))
        
        # Mostrar texto
        vida_text = font_small.render(f"{self.nombre}: {self.vida_actual}/{self.vida_max}", True, YELLOW)
        screen.blit(vida_text, (x, y + 35))
        
        # Mostrar especiales restantes
        especial_text = font_small.render(f"Especiales: {self.especiales}", True, YELLOW)
        screen.blit(especial_text, (x, y + 60))

def mostrar_mensaje(mensaje, y_pos=350, color=YELLOW):
    texto = font_large.render(mensaje, True, color)
    screen.blit(texto, (widthq // 2 - texto.get_width() // 2, y_pos))
    pyg.display.flip()
