import pygame as pyg
import sys
import funciones as fun

pyg.init()
screen = pyg.display.set_mode((fun.heightq, fun.widthq), pyg.RESIZABLE)
pyg.display.set_caption("FFFFFFFF")

background_original= pyg.image.load("img/base_ciudad.jpg").convert()

background_juego= fun.size_imgen(background_original, screen)
screen.blit(background_juego, (0, 0))

clock_fps = pyg.time.Clock()
running = True

while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        elif event.type == pyg.VIDEORESIZE:
            background_juego= fun.size_imgen(background_juego, screen)
    screen.blit(background_juego, (0, 0))
    
    pyg.display.flip()
    pyg.display.update()
    clock_fps.tick(60)  # limits FPS to 60

pyg.quit()
sys.exit()