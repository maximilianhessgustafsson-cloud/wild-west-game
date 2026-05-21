import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init() 

SKÄRMENS_BREDD = 1864
SKÄRMENS_HÖJD = 1082

screen = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Bridge Shootout")
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

# --- Ladda Grafik ---
background = pygame.image.load("C:/spel/grafik/bakgrund/background.png").convert()
jeem_img = pygame.image.load("C:/spel/grafik/pngs/Jeem.png").convert_alpha()
jeem_img = pygame.transform.scale(jeem_img, (80, 80)) 

crosshair = pygame.image.load("C:/spel/grafik/pngs/crosshair.png").convert_alpha()
crosshair = pygame.transform.scale(crosshair, (50, 50))

aurameny = pygame.image.load("C:/spel/grafik/pngs/jagaura.png").convert_alpha()
aurameny = pygame.transform.scale(aurameny, (1000, 1000)) 

# Ladda och skala tungtung.png - Nu mycket större (500x500)
tungtung_img = pygame.image.load("C:/spel/grafik/pngs/tungtung.png").convert_alpha()
tungtung_img = pygame.transform.scale(tungtung_img, (500, 500)) 

# --- Ladda Ljud ---
gun_sound = pygame.mixer.Sound("C:/spel/audio/gun.mp3")

# Ladda ljudet för Tung Tung när han dyker upp
tungtung_intro_sound = pygame.mixer.Sound("C:/spel/audio/tungtungsahur.mp3")

pygame.mixer.music.load("C:/spel/audio/menymusik.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) 

# --- Typsnitt ---
timer_font = pygame.font.SysFont("Arial", 48, bold=True)
game_over_font = pygame.font.SysFont("Arial", 120, bold=True)
titel_font = pygame.font.SysFont("Arial", 120, bold=True)
knapp_font = pygame.font.SysFont("Arial", 60, bold=True)

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

# --- Spelvariabler ---
START_TID_MINUTER = 3
total_sekunder = START_TID_MINUTER * 60
start_ticks = 0
spel_status = "meny" 

# Variabler för tungtung-animationen i menyn
tungtung_x = SKÄRMENS_BREDD
tungtung_y = 0
tungtung_aktiv = False
last_tungtung_time = pygame.time.get_ticks()

# Positionera knappar
VÄNSTER_PANEL_X = SKÄRMENS_BREDD // 3
start_knapp = pygame.Rect(VÄNSTER_PANEL_X - 150, 550, 300, 80)
exit_knapp = pygame.Rect(VÄNSTER_PANEL_X - 150, 700, 300, 80)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if spel_status == "meny":
                gun_sound.play()
                
                if start_knapp.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    spel_status = "spelar"
                    start_ticks = pygame.time.get_ticks()
                elif exit_knapp.collidepoint(mouse_pos):
                    running = False

    # --- Rita ---
    screen.blit(background, (0, 0))

    if spel_status == "meny":
        nuvarande_tid = pygame.time.get_ticks()
        # Logik för att starta tungtung var 15:e sekund
        if not tungtung_aktiv and nuvarande_tid - last_tungtung_time >= 15000:
            tungtung_aktiv = True
            tungtung_x = SKÄRMENS_BREDD
            
            # Justerat Y-slump för att passa större storlek (slutar högre upp så han inte åker i golvet)
            tungtung_y = random.randint(50, SKÄRMENS_HÖJD - 550) 
            
            # Spela introljudet!
            tungtung_intro_sound.play()
            last_tungtung_time = nuvarande_tid

        # Logik för att flytta tungtung till vänster
        if tungtung_aktiv:
            tungtung_x -= 12
            if tungtung_x < -500: # Matchar den nya bredden (500)
                tungtung_aktiv = False

        # --- RIT-ORDNING ÄNDRAD HÄR FÖR LAGERHÅLLNING ---

        # 1. Rita den stora stationära karaktären till höger (Längst bak)
        aura_rect = aurameny.get_rect(bottomright=(SKÄRMENS_BREDD, SKÄRMENS_HÖJD))
        screen.blit(aurameny, aura_rect)

        # 2. Rita Titel och Knappar (Mellanlagret)
        titel_text = titel_font.render("Bridge Shootout", True, (255, 255, 255))
        titel_rect = titel_text.get_rect(center=(VÄNSTER_PANEL_X, 300))
        titel_skugga = titel_font.render("Bridge Shootout", True, (0, 0, 0))
        screen.blit(titel_skugga, (titel_rect.x + 5, titel_rect.y + 5))
        screen.blit(titel_text, titel_rect)

        pygame.draw.rect(screen, (34, 139, 34), start_knapp, border_radius=10) 
        pygame.draw.rect(screen, (178, 34, 34), exit_knapp, border_radius=10)  

        start_text = knapp_font.render("START", True, (255, 255, 255))
        exit_text = knapp_font.render("EXIT", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=start_knapp.center))
        screen.blit(exit_text, exit_text.get_rect(center=exit_knapp.center))

        # 3. Rita Tung Tung (Framför text/knappar, men bakom hårkorset)
        if tungtung_aktiv:
            screen.blit(tungtung_img, (tungtung_x, tungtung_y))

    elif spel_status == "spelar":
        # (Oändrad spellogik)
        sekunder_sedan_start = (pygame.time.get_ticks() - start_ticks) // 1000
        återstående_sekunder = total_sekunder - sekunder_sedan_start

        if återstående_sekunder <= 0:
            återstående_sekunder = 0
            spel_status = "game_over"

        minuter = återstående_sekunder // 60
        sekunder = återstående_sekunder % 60
        timer_text_str = f"{minuter:02}:{sekunder:02}" 

        jeem_target.update()
        jeem_target.draw(screen)

        timer_text_yta = timer_font.render(timer_text_str, True, (255, 255, 255))
        screen.blit(timer_text_yta, (20, 20))

    elif spel_status == "game_over":
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SKÄRMENS_BREDD // 2, SKÄRMENS_HÖJD // 2))
        screen.blit(game_over_text, text_rect)

    # Rita alltid hårkorset sist (Absolut överst)
    screen.blit(crosshair, (mouse_pos[0] - 25, mouse_pos[1] - 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()