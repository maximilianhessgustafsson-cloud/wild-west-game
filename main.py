import pygame
import random

pygame.init()

SKÄRMENS_BREDD = 1864
SKÄRMENS_HÖJD = 1082

screen = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))
pygame.display.set_caption("Wild West")
clock = pygame.time.Clock()

background = pygame.image.load("C:/spel/grafik/bakgrund/background.png")
jeem_img = pygame.image.load("C:/spel/grafik/pngs/Jeem.png").convert_alpha()
jeem_img = pygame.transform.scale(jeem_img, (80, 80)) 

class Target:
    def __init__(self, img):
        self.image = img
        self.rect = self.image.get_rect()
        self.is_visible = False
        self.display_duration = 2000 
        self.next_pop_time = pygame.time.get_ticks() + random.randint(500, 2000)
        self.start_time = 0

    def spawn(self):
        self.is_visible = True
        self.rect.x = random.randint(100, SKÄRMENS_BREDD - 100)
        self.rect.y = random.randint(100, SKÄRMENS_HÖJD - 250)
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if not self.is_visible:
            if current_time >= self.next_pop_time:
                self.spawn()
        else:
            if current_time - self.start_time >= self.display_duration:
                self.is_visible = False
                self.next_pop_time = current_time + random.randint(1000, 3000)

    def draw(self, surface):
        if self.is_visible:
            surface.blit(self.image, self.rect)

jeem_target = Target(jeem_img)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

    jeem_target.update()

    screen.blit(background, (0, 0))
    jeem_target.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()