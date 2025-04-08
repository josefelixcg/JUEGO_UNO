import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Combate")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fuentes
font_large = pygame.font.SysFont('Arial', 36)
font_medium = pygame.font.SysFont('Arial', 24)
font_small = pygame.font.SysFont('Arial', 18)

class Contrincante:
    def __init__(self, nombre, vida, color):
        self.nombre = nombre
        self.vida_max = vida
        self.vida_actual = vida
        self.color = color
        self.ataques = []
        self.especiales = 3  # Número de ataques especiales disponibles
        
    def atacar(self, tipo_ataque, oponente):
        if tipo_ataque == "normal":
            danio = 10
            oponente.vida_actual -= danio
            return f"{self.nombre} usa ataque normal! (-{danio} vida)"
        elif tipo_ataque == "especial" and self.especiales > 0:
            danio = 15
            oponente.vida_actual -= danio
            self.especiales -= 1
            return f"{self.nombre} usa ataque especial! (-{danio} vida)"
        else:
            return "Ataque especial no disponible o inválido"
    
    def dibujar(self, x, y):
        # Dibujar barra de vida
        pygame.draw.rect(screen, BLACK, (x, y, 200, 30), 2)
        vida_width = int(200 * (self.vida_actual / self.vida_max))
        pygame.draw.rect(screen, self.color, (x, y, vida_width, 30))
        
        # Mostrar texto
        vida_text = font_small.render(f"{self.nombre}: {self.vida_actual}/{self.vida_max}", True, BLACK)
        screen.blit(vida_text, (x, y + 35))
        
        # Mostrar especiales restantes
        especial_text = font_small.render(f"Especiales: {self.especiales}", True, BLACK)
        screen.blit(especial_text, (x, y + 60))

def mostrar_mensaje(mensaje, y_pos=250, color=BLACK):
    texto = font_medium.render(mensaje, True, color)
    screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, y_pos))
    pygame.display.flip()

def main():
    pc = Contrincante("PC", 90, RED)
    usuario = Contrincante("Usuario", 100, GREEN)
    
    turno = None
    esperando_input = False
    mensaje = ""
    resultado = ""
    
    clock = pygame.time.Clock()
    running = True
    
    while running and pc.vida_actual > 0 and usuario.vida_actual > 0:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not esperando_input:
                    # Determinar quién ataca
                    turno = random.randint(1, 2)
                    if turno == 1:
                        mensaje = "ATACA PC!"
                        # PC ataca aleatoriamente
                        ataque_pc = random.choice(["normal", "especial"] if pc.especiales > 0 else ["normal"])
                        mensaje += "\n" + pc.atacar(ataque_pc, usuario)
                    else:
                        mensaje = "ATACA USUARIO!"
                        esperando_input = True
                elif esperando_input:
                    if event.key == pygame.K_a:
                        mensaje = "Usuario usa lanza! (-10 vida)"
                        usuario.atacar("normal", pc)
                        esperando_input = False
                    elif event.key == pygame.K_b and usuario.especiales > 0:
                        mensaje = "Usuario usa sable! (-15 vida)"
                        usuario.atacar("especial", pc)
                        esperando_input = False
                    elif event.key == pygame.K_b and usuario.especiales <= 0:
                        mensaje = "No te quedan ataques especiales!"
        
        # Dibujar los contrincantes
        pc.dibujar(100, 100)
        usuario.dibujar(500, 100)
        
        # Mostrar instrucciones
        if not esperando_input:
            instrucciones = font_small.render("Presiona ENTER para continuar", True, BLUE)
            screen.blit(instrucciones, (WIDTH // 2 - instrucciones.get_width() // 2, 400))
        else:
            instrucciones = font_small.render("Elige ataque: [A]Lanza (-10)  [B]Sable (-15)", True, BLUE)
            screen.blit(instrucciones, (WIDTH // 2 - instrucciones.get_width() // 2, 400))
        
        # Mostrar mensaje de turno
        if mensaje:
            lineas = mensaje.split('\n')
            for i, linea in enumerate(lineas):
                mostrar_mensaje(linea, 250 + i * 30)
        
        pygame.display.flip()
        clock.tick(30)
    
    # Determinar el resultado final
    if pc.vida_actual <= 0 and usuario.vida_actual <= 0:
        resultado = "Empate!"
    elif pc.vida_actual <= 0:
        resultado = "EL GANADOR ES EL USUARIO!"
    else:
        resultado = "TE GANO LA PC."
    
    # Pantalla final
    screen.fill(WHITE)
    texto_resultado = font_large.render(resultado, True, BLACK)
    screen.blit(texto_resultado, (WIDTH // 2 - texto_resultado.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    
    # Esperar antes de salir
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()