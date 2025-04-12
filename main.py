import pygame as pyg
import sys
import funciones as fun
import random
#CAMBIO
pyg.init()

screen = pyg.display.set_mode((fun.heightq, fun.widthq), pyg.RESIZABLE)
pyg.display.set_caption("JUEGO UNO")

usuario= fun.User("FELIX", 100, fun.GREEN)
pc = fun.User("P. C.", 100, fun.RED)

background_original= pyg.image.load("img/base_ciudad.jpg").convert()

background_juego= fun.size_imgen(background_original, screen)
screen.blit(background_juego, (0, 0))

clock_fps = pyg.time.Clock()
running = True

esperando_input = False
turno = None
mensaje = ""
resultado = ""

while running and pc.vida_actual > 0 and usuario.vida_actual > 0:
    usuario.posicionamiento(100, 100)
    pc.posicionamiento(500, 100)
    mensaje =""
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
           running = False
        elif event.type == pyg.VIDEORESIZE:
            background_juego= fun.size_imgen(background_juego, screen)
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_RETURN and not esperando_input:
                    turno = random.randint(1, 2)
                    if turno == 1:
                        mensaje = "ATACA PC!"
                        ataque_pc = random.choice(["NORMAL", "ESPECIAL"] if pc.especiales > 0 else ["NORMAL"])
                        mensaje += "\n" + pc.attack(ataque_pc, usuario)
                    else:
                        mensaje = "ATACA USUARIO!"
                        esperando_input = True
            elif esperando_input:
                    if event.key == pyg.K_a:
                        mensaje = "Usuario usa lanza! (-10 vida)"
                        usuario.attack("NORMAL", pc)
                        esperando_input = False
                    elif event.key == pyg.K_b and usuario.especiales > 0:
                        mensaje = "Usuario usa sable! (-15 vida)"
                        usuario.attack("ESPECIAL", pc)
                        esperando_input = False
                    elif event.key == pyg.K_b and usuario.especiales <= 0:
                        mensaje = "No te quedan ataques especiales!"
    
    # Mostrar instrucciones
    if not esperando_input:
            instrucciones = fun.font_small.render("Presiona ENTER para continuar", True, fun.YELLOW)
            screen.blit(instrucciones, (fun.widthq // 2 - instrucciones.get_width() // 2, 400))
    else:
        instrucciones = fun.font_small.render("Elige ataque: [A]Lanza (-10)  [B]Sable (-15)", True, fun.YELLOW)
        screen.blit(instrucciones, (fun.widthq // 2 - instrucciones.get_width() // 2, 300))    
        
        # Mostrar mensaje de turno
        if mensaje:
            lineas = mensaje.split('\n')
            for i, linea in enumerate(lineas):
                fun.mostrar_mensaje(linea, 350 + i * 20)    

    pyg.display.flip()
    pyg.display.update()
    clock_fps.tick(60)  # limits FPS to 60

pyg.quit()
sys.exit()
