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


class Target:
    def __init__(self, img):
        self.image = img
        self.rect = self.image.get_rect()
        self.is_visible = False
        self.timer = 0
        self.display_duration = 1200 # How long Jeem stays up
        self.next_pop_time = pygame.time.get_ticks() + random.randint(500, 3000)

    def spawn(self):
        self.is_visible = True
        self.rect.x = random.randint(100, SKÄRMENS_BREDD - 100)
        self.rect.y = random.randint(100, SKÄRMENS_HÖJD - 250) # Keep him above the "counter"
        self.timer = pygame.time.get_ticks()



running = True



















while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

   
    screen.blit(background, (0, 0))

    
    pygame.display.flip()


pygame.quit()