import pygame
import random

pygame.init()

SKÄRMENS_BREDD = 1864
SKÄRMENS_HÖJD = 1082

screen = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

pygame.display.set_caption("Wild West")

background = pygame.image.load("C:/spel/grafik/bakgrund/background.png")
Jeem = pygame.image.load("C:/spel/grafik/pngs/Jeem.png").convert_alpha()
Jeem = pygame.transform.scale(Jeem, (80, 80)) 








running = True



















while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

   
    screen.blit(background, (0, 0))

    
    pygame.display.flip()


pygame.quit()