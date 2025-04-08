import pygame as pyg
import os
heightq, widthq = 900, 450

def size_imgen(background_original, screen):
    ventana= screen.get_size()
    return pyg.transform.scale(background_original, ventana)

class Personaje:
    def __init__(self, nombre, x, y, ancho, alto):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.vida = 100
        self.lanzas_restantes = 3
        self.zables_restantes = 3
        
        # Cargar imágenes
        self.imagen_normal = None
        self.imagen_ataque = None
        self.imagen_defensa = None
        self.imagen_actual = None
        
        # Rectángulo para colisiones/posición
        self.rect = pyg.Rect(x, y, ancho, alto)
    
    def cargar_imagenes(self, ruta_normal, ruta_ataque, ruta_defensa):
        """Carga las imágenes para los diferentes estados del personaje"""
        try:
            self.imagen_normal = pyg.image.load(ruta_normal)
            self.imagen_ataque = pyg.image.load(ruta_ataque)
            self.imagen_defensa = pyg.image.load(ruta_defensa)
            self.imagen_normal = pyg.transform.scale(self.imagen_normal, (self.ancho, self.alto))
            self.imagen_ataque = pyg.transform.scale(self.imagen_ataque, (self.ancho, self.alto))
            self.imagen_defensa = pyg.transform.scale(self.imagen_defensa, (self.ancho, self.alto))
            self.imagen_actual = self.imagen_normal
            return True
        except:
            print(f"Error al cargar imágenes para {self.nombre}")
            return False
    
    def atacar(self, arma):
        """Cambia a la imagen de ataque y reduce el arma correspondiente"""
        if arma == "LANZA" and self.lanzas_restantes > 0:
            self.lanzas_restantes -= 1
            self.imagen_actual = self.imagen_ataque
            return True
        elif arma == "ZABLE" and self.zables_restantes > 0:
            self.zables_restantes -= 1
            self.imagen_actual = self.imagen_ataque
            return True
        return False
    
    def defender(self):
        """Cambia a la imagen de defensa"""
        self.imagen_actual = self.imagen_defensa
    
    def reset_estado(self):
        """Vuelve a la imagen normal"""
        self.imagen_actual = self.imagen_normal
    
    def recibir_dano(self, cantidad):
        """Reduce la vida del personaje"""
        self.vida = max(0, self.vida - cantidad)
    
    def dibujar(self, pantalla):
        """Dibuja el personaje en la pantalla"""
        if self.imagen_actual:
            pantalla.blit(self.imagen_actual, (self.x, self.y))
        
        # Dibujar barra de vida
        pyg.draw.rect(pantalla, (255, 0, 0), (self.x, self.y - 20, self.ancho, 10))
        pyg.draw.rect(pantalla, (0, 255, 0), (self.x, self.y - 20, self.ancho * (self.vida / 100), 10))
        
        # Mostrar inventario (solo para el jugador)
        if self.nombre == "Jugador":
            fuente = pyg.font.SysFont(None, 24)
            texto_lanzas = fuente.render(f"Lanzas: {self.lanzas_restantes}", True, (255, 255, 255))
            texto_zables = fuente.render(f"Zables: {self.zables_restantes}", True, (255, 255, 255))
            pantalla.blit(texto_lanzas, (self.x, self.y + self.alto + 10))
            pantalla.blit(texto_zables, (self.x, self.y + self.alto + 30))