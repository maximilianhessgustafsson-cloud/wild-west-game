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

caspej_img = pygame.image.load("C:/spel/grafik/pngs/Caspej.png").convert_alpha()
caspej_img = pygame.transform.scale(caspej_img, (80, 80))

crosshair = pygame.image.load("C:/spel/grafik/pngs/crosshair.png").convert_alpha()
crosshair = pygame.transform.scale(crosshair, (50, 50))

aurameny = pygame.image.load("C:/spel/grafik/pngs/jagaura.png").convert_alpha()
aurameny = pygame.transform.scale(aurameny, (1000, 1000)) 

tungtung_img = pygame.image.load("C:/spel/grafik/pngs/tungtung.png").convert_alpha()
tungtung_img = pygame.transform.scale(tungtung_img, (500, 500)) 

jam_img = pygame.image.load("C:/spel/grafik/pngs/JAM.png").convert_alpha()
jam_img = pygame.transform.scale(jam_img, (500, 500))

# Ladda erm.png
erm_img = pygame.image.load("C:/spel/grafik/pngs/erm.png").convert_alpha()
erm_img = pygame.transform.scale(erm_img, (500, 500))

# --- Ladda Ljud ---
gun_sound = pygame.mixer.Sound("C:/spel/audio/gun.mp3")
gun_gameplay_sound = pygame.mixer.Sound("C:/spel/audio/gun_gameplay.mp3")
tungtung_intro_sound = pygame.mixer.Sound("C:/spel/audio/tungtungsahur.mp3")
yophon_sound = pygame.mixer.Sound("C:/spel/audio/yophon.mp3")
silver_sound = pygame.mixer.Sound("C:/spel/audio/silver.mp3")

# Starta menymusiken direkt vid uppstart
pygame.mixer.music.load("C:/spel/audio/menymusik.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) 

timer_font = pygame.font.SysFont("Arial", 48, bold=True)
game_over_font = pygame.font.SysFont("Arial", 120, bold=True)
titel_font = pygame.font.SysFont("Arial", 120, bold=True)
knapp_font = pygame.font.SysFont("Arial", 60, bold=True)

class Target:
    def __init__(self, jeem_img, caspej_img):
        self.jeem_image = jeem_img
        self.caspej_image = caspej_img
        self.image = jeem_img
        self.rect = self.image.get_rect()
        self.is_visible = False
        self.display_duration = 2000 
        self.next_pop_time = pygame.time.get_ticks() + random.randint(500, 2000)
        self.start_time = 0
        
        self.is_caspej = False
        self.jeem_spawn_count = 0

    def spawn(self):
        self.is_visible = True
        
        if self.jeem_spawn_count >= 3:
            self.jeem_spawn_count = 0 
            
            if random.random() < 0.5: 
                self.is_caspej = True
                self.image = self.caspej_image
            else:
                self.is_caspej = False
                self.image = self.jeem_image
                self.jeem_spawn_count += 1 
        else:
            self.is_caspej = False
            self.image = self.jeem_image
            self.jeem_spawn_count += 1 

        self.rect = self.image.get_rect()
        
        while True:
            self.rect.x = random.randint(100, SKÄRMENS_BREDD - 100)
            self.rect.y = random.randint(100, SKÄRMENS_HÖJD - 250)
            
            if not (self.rect.x < 450 and self.rect.y < 220):
                break 

        self.start_time = pygame.time.get_ticks()

    def update(self, display_duration, cooldown_range):
        current_time = pygame.time.get_ticks()
        
        if not self.is_visible:
            if current_time >= self.next_pop_time:
                self.spawn()
            return "inget"
        else:
            if current_time - self.start_time >= display_duration:
                self.is_visible = False
                self.next_pop_time = current_time + random.randint(cooldown_range[0], cooldown_range[1])
                
                if self.is_caspej:
                    return "caspej_miss"
                else:
                    return "jeem_miss"
            return "inget"

    def draw(self, surface):
        if self.is_visible:
            surface.blit(self.image, self.rect)

jeem_target = Target(jeem_img, caspej_img)

START_TID_MINUTER = 3
total_sekunder = START_TID_MINUTER * 60
start_ticks = 0
spel_status = "meny" 
score = 0

current_duration = 2000
current_cooldown = (1000, 3000)
niva_text_str = "Nivå: 1"

# --- Variabler för tungtung ---
tungtung_x = SKÄRMENS_BREDD
tungtung_y = 0
tungtung_aktiv = False
last_tungtung_time = pygame.time.get_ticks()

# --- Variabler för JAM ---
jam_x = 0
jam_y = SKÄRMENS_HÖJD
jam_aktiv = False
last_jam_time = pygame.time.get_ticks()

# --- Variabler för Erm ---
erm_aktiv = False
erm_start_tid = 0

# --- Knappar för Meny ---
VÄNSTER_PANEL_X = SKÄRMENS_BREDD // 3
start_knapp = pygame.Rect(VÄNSTER_PANEL_X - 150, 550, 300, 80)
exit_knapp = pygame.Rect(VÄNSTER_PANEL_X - 150, 700, 300, 80)

# Knappar för Game Over
restart_knapp = pygame.Rect(SKÄRMENS_BREDD // 2 - 320, SKÄRMENS_HÖJD // 2 + 150, 300, 80)
meny_knapp = pygame.Rect(SKÄRMENS_BREDD // 2 + 20, SKÄRMENS_HÖJD // 2 + 150, 300, 80)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    aura_rect = aurameny.get_rect(bottomright=(SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if spel_status == "meny":
                if start_knapp.collidepoint(mouse_pos):
                    gun_sound.play()
                    
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("C:/spel/audio/larp.mp3")
                    pygame.mixer.music.play(-1)
                    
                    spel_status = "spelar"
                    start_ticks = pygame.time.get_ticks()
                    score = 0
                    total_sekunder = START_TID_MINUTER * 60
                    jeem_target.jeem_spawn_count = 0 
                elif exit_knapp.collidepoint(mouse_pos):
                    gun_sound.play()
                    running = False
                elif aura_rect.collidepoint(mouse_pos):
                    silver_sound.play()
                    erm_aktiv = True
                    erm_start_tid = pygame.time.get_ticks()
                else:
                    gun_sound.play()
            
            elif spel_status == "spelar":
                if jeem_target.is_visible and jeem_target.rect.collidepoint(mouse_pos):
                    gun_gameplay_sound.play()
                    jeem_target.is_visible = False
                    jeem_target.next_pop_time = pygame.time.get_ticks() + random.randint(current_cooldown[0], current_cooldown[1])
                    
                    if jeem_target.is_caspej:
                        score += 50 
                    else:
                        score += 10
                        total_sekunder += 5 
                else:
                    gun_sound.play()
                    total_sekunder -= 15 

            elif spel_status == "game_over":
                if restart_knapp.collidepoint(mouse_pos):
                    gun_sound.play()
                    
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("C:/spel/audio/larp.mp3")
                    pygame.mixer.music.play(-1)
                    
                    spel_status = "spelar"
                    start_ticks = pygame.time.get_ticks()
                    score = 0
                    total_sekunder = START_TID_MINUTER * 60
                    jeem_target.jeem_spawn_count = 0
                    jeem_target.is_visible = False
                elif meny_knapp.collidepoint(mouse_pos):
                    gun_sound.play()
                    spel_status = "meny"
                    
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("C:/spel/audio/menymusik.mp3")
                    pygame.mixer.music.play(-1)

    screen.blit(background, (0, 0))

    if spel_status == "meny":
        nuvarande_tid = pygame.time.get_ticks()
        
        # --- Logik för tungtung ---
        if not tungtung_aktiv and nuvarande_tid - last_tungtung_time >= 15000:
            tungtung_aktiv = True
            tungtung_x = SKÄRMENS_BREDD
            tungtung_y = random.randint(50, SKÄRMENS_HÖJD - 550) 
            tungtung_intro_sound.play()
            last_tungtung_time = nuvarande_tid

        if tungtung_aktiv:
            tungtung_x -= 12
            if tungtung_x < -500:
                tungtung_aktiv = False

        # --- Logik för JAM (Ändrad till 20000 ms / 20 sekunder) ---
        if not jam_aktiv and nuvarande_tid - last_jam_time >= 20000:
            jam_aktiv = True
            jam_y = SKÄRMENS_HÖJD 
            jam_x = random.randint(100, SKÄRMENS_BREDD - 600) 
            yophon_sound.play() 
            last_jam_time = nuvarande_tid

        if jam_aktiv:
            jam_y -= 12 
            if jam_y < -500: 
                jam_aktiv = False

        screen.blit(aurameny, aura_rect)

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

        if tungtung_aktiv:
            screen.blit(tungtung_img, (tungtung_x, tungtung_y))
            
        if jam_aktiv:
            screen.blit(jam_img, (jam_x, jam_y))

        if erm_aktiv:
            if nuvarande_tid - erm_start_tid < 17000: 
                erm_rect = erm_img.get_rect(center=(SKÄRMENS_BREDD // 2, SKÄRMENS_HÖJD // 2))
                screen.blit(erm_img, erm_rect)
            else:
                erm_aktiv = False 

    elif spel_status == "spelar":
        last_tungtung_time = pygame.time.get_ticks()
        last_jam_time = pygame.time.get_ticks()

        sekunder_sedan_start = (pygame.time.get_ticks() - start_ticks) // 1000
        återstående_sekunder = total_sekunder - sekunder_sedan_start

        if återstående_sekunder <= 0:
            återstående_sekunder = 0
            spel_status = "game_over"

        if sekunder_sedan_start < 15:
            current_duration = 2000      
            current_cooldown = (1000, 3000) 
            niva_text_str = "Nivå: 1"
        elif sekunder_sedan_start < 30:
            current_duration = 1300      
            current_cooldown = (500, 1500)  
            niva_text_str = "Level: 2 (Faster!)"
        else:
            current_duration = 700       
            current_cooldown = (200, 700)   
            niva_text_str = "Level: 3 (Even faster!)"

        minuter = återstående_sekunder // 60
        sekunder = återstående_sekunder % 60
        timer_text_str = f"{minuter:02}:{sekunder:02}" 

        resultat = jeem_target.update(current_duration, current_cooldown)
        if resultat == "jeem_miss":
            total_sekunder -= 10
        elif resultat == "caspej_miss":
            total_sekunder -= 60 

        jeem_target.draw(screen)

        timer_text_yta = timer_font.render(timer_text_str, True, (255, 255, 255))
        screen.blit(timer_text_yta, (20, 20))

        score_text_yta = timer_font.render(f"Points: {score}", True, (255, 255, 255))
        screen.blit(score_text_yta, (20, 80))

        niva_text_yta = timer_font.render(niva_text_str, True, (255, 215, 0)) 
        screen.blit(niva_text_yta, (20, 140))

    elif spel_status == "game_over":
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SKÄRMENS_BREDD // 2, SKÄRMENS_HÖJD // 2 - 50))
        screen.blit(game_over_text, text_rect)

        final_score_text = timer_font.render(f"Din slutpoäng: {score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(SKÄRMENS_BREDD // 2, SKÄRMENS_HÖJD // 2 + 60))
        screen.blit(final_score_text, final_score_rect)

        pygame.draw.rect(screen, (34, 139, 34), restart_knapp, border_radius=10) 
        pygame.draw.rect(screen, (70, 130, 180), meny_knapp, border_radius=10)   

        restart_text = knapp_font.render("RESTART", True, (255, 255, 255))
        meny_text = knapp_font.render("MENU", True, (255, 255, 255))
        
        screen.blit(restart_text, restart_text.get_rect(center=restart_knapp.center))
        screen.blit(meny_text, meny_text.get_rect(center=meny_knapp.center))

    screen.blit(crosshair, (mouse_pos[0] - 25, mouse_pos[1] - 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()