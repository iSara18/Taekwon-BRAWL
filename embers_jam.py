import pygame
from sys import exit
from random import randint, choice
import os, sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# initialize stamina
stamina_num = 4

# initialize health
health_num = 4

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_idle = pygame.image.load(resource_path('graphics/player/idle.png')).convert_alpha()
        player_bounce = pygame.image.load(resource_path('graphics/player/bounce.png')).convert_alpha()

        self.player_idling = [player_idle,player_bounce]
        self.player_index = 0
        self.player_jump = pygame.image.load(resource_path('graphics/player/jump.png')).convert_alpha()
        self.player_kick = pygame.image.load(resource_path('graphics/player/kick.png')).convert_alpha()

        self.image = self.player_idling[self.player_index]
        self.rect = self.image.get_rect(center = (320, 280))
        self.gravity = 0
        self.kick = False
        self.player_attacking = False
        self.num_kicks = 0

        self.jump_sound = pygame.mixer.Sound(resource_path('audio/jump_audio.mp3'))
        self.jump_sound.set_volume(0.5)

        self.kick_sound = pygame.mixer.Sound(resource_path('audio/kick_audio.mp3'))
        self.kick_sound.set_volume(0.3)

    def player_input(self):
        global stamina_num

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 286 and stamina_num > 0:
            self.gravity = -10
            stamina_num -= 1
            self.jump_sound.play()

        if keys[pygame.K_UP] and self.rect.bottom == 286:
            self.kick = True
            self.kick_sound.play()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        
    def player_attack(self):
        if self.rect.bottom < 286:
            self.player_attacking = True
        else: self.player_attacking = False
        return self.player_attacking

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 286:
            self.rect.bottom = 286

    def animation_state(self):
        if self.rect.bottom < 286:
            self.image = self.player_jump
        
        elif self.kick == True:
            self.player_attacking = True
            self.image = self.player_kick
            self.kick = False

        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_idling): self.player_index = 0
            self.image = self.player_idling[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.player_attack()
        self.apply_gravity()
        self.animation_state()

class Opps(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'blue':
            b_idle = pygame.image.load(resource_path('graphics/opps/blue/b_idle.png')).convert_alpha()
            b_bounce = pygame.image.load(resource_path('graphics/opps/blue/b_bounce.png')).convert_alpha()
            self.frames = [b_idle,b_bounce,b_idle,b_bounce]
            self.kick = pygame.image.load(resource_path('graphics/opps/blue/b_kick.png')).convert_alpha()
        else:
            p_idle = pygame.image.load(resource_path('graphics/opps/pink/p_idle.png')).convert_alpha()
            p_bounce = pygame.image.load(resource_path('graphics/opps/pink/p_bounce.png')).convert_alpha()
            self.frames = [p_idle,p_bounce,p_idle,p_bounce]
            self.kick = pygame.image.load(resource_path('graphics/opps/pink/p_jump.png')).convert_alpha()
        
        self.opps_attacking = False
        self.gravity = 0
        self.y_pos = 286
        self.animation_index = 0
        self.frames.append(self.kick)
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(660,900),self.y_pos))

    def opps_attack(self):
        if self.image is self.kick:
            self.opps_attacking = True
        else: self.opps_attacking = False
        return self.opps_attacking

    def animation_state(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        self.opps_attack()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Stamina(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # player stamina
        stamina_1 = pygame.image.load(resource_path('graphics/stamina/1_stamina.png')).convert_alpha()
        stamina_2 = pygame.image.load(resource_path('graphics/stamina/2_stamina.png')).convert_alpha()
        stamina_3 = pygame.image.load(resource_path('graphics/stamina/3_stamina.png')).convert_alpha()
        stamina_4 = pygame.image.load(resource_path('graphics/stamina/4_stamina.png')).convert_alpha()

        self.staminas = [stamina_1, stamina_2, stamina_3, stamina_4]
        self.image = stamina_4 #self.staminas[stamina - 1]
        self.rect = self.image.get_rect(center = (321, 225))
    
    def update_available_stamina(self): 
        global stamina_num

        if stamina_num == 4:
            self.image = self.staminas[3]
        elif stamina_num == 3:
            self.image = self.staminas[2]
        elif stamina_num == 2:
            self.image = self.staminas[1]
        elif stamina_num == 1:
            self.image = self.staminas[0]            
        elif stamina_num < 1:
            self.image = pygame.Surface((0, 0))
 
    def update(self):
        self.update_available_stamina()

class Health(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # player health
        health_1 = pygame.image.load(resource_path('graphics/health/1_health.png')).convert_alpha()
        health_2 = pygame.image.load(resource_path('graphics/health/2_health.png')).convert_alpha()
        health_3 = pygame.image.load(resource_path('graphics/health/3_health.png')).convert_alpha()
        health_4 = pygame.image.load(resource_path('graphics/health/4_health.png')).convert_alpha()

        self.hearts = [health_1, health_2, health_3, health_4]
        self.image = health_4
        self.rect = self.image.get_rect(center = (321, 225))
    
    def update_available_hearts(self): 
        global health_num

        if health_num == 4:
            self.image = self.hearts[3]
        elif health_num == 3:
            self.image = self.hearts[2]
        elif health_num == 2:
            self.image = self.hearts[1]
        elif health_num == 1:
            self.image = self.hearts[0]            
        # elif health_num < 1:
        #     self.image = pygame.Surface((0, 0))
 
    def update(self):
        self.update_available_hearts()

def check_collision():
    global score, health_num

    if player.sprite.player_attacking and pygame.sprite.spritecollide(player.sprite,opps, True):
        score += 1
        return True
    elif (not player.sprite.player_attacking) and pygame.sprite.spritecollide(player.sprite,opps, True) and health_num >= 1:
        health_num -= 1
        if health_num == 0:
            return False
        return True
    elif (not player.sprite.player_attacking) and pygame.sprite.spritecollide(player.sprite, opps, False) and health_num < 1:
        return False
    return True

def collisions():
    if pygame.sprite.spritecollide(player.sprite,opps,True) and player.sprite.player_attacking:
        collision_numb += 1
        return collision_numb
        
def display_score():
    score_surf = font.render(f'{score}',False,'BLACK')
    score_rect = score_surf.get_rect(center = (352,38))
    screen.blit(score_surf,score_rect)
    return score

# pause menu bool
pause_on = False

pygame.init()
screen = pygame.display.set_mode((640, 448))
pygame.display.set_caption('Taekwon-BRAWL')
clock = pygame.time.Clock()
game_active = False
score = 0
collision_numb = 0
bg_music = pygame.mixer.Sound(resource_path('audio/bg_music.mp3'))
# bg_music.play(loops = -1)

# Groups

player = pygame.sprite.GroupSingle()
player.add(Player())

opps = pygame.sprite.Group()

stamina = pygame.sprite.GroupSingle()

health = pygame.sprite.GroupSingle()

# Intro Screen

font = pygame.font.Font(resource_path('font/Pixeltype.ttf'), 50)

game_name = font.render('Taekwon-BRAWL',False,'BLACK')
game_name_rect = game_name.get_rect(center = (320,100))

game_message = font.render('Press [Space] to Start!',False,'BLACK')
game_message_rect = game_message.get_rect(center = (320,150))

bg = pygame.image.load(resource_path('graphics/tkd_bg.png')).convert()
start_screen = pygame.image.load(resource_path('graphics/start_screen.png')).convert()

# pause button

pause_shadow = pygame.image.load("graphics/button/q_shadow.png").convert_alpha()
pause_shadow_rect = pause_shadow.get_rect(topright = (634,6))
pause_down = pygame.image.load(resource_path("graphics/button/q_pressed.png")).convert_alpha()
pause_down_rect = pause_down.get_rect(topright = (634,6))

pause = pygame.image.load(resource_path('graphics/pause_menu.png')).convert_alpha()

# Timer
opps_timer = pygame.USEREVENT + 1
pygame.time.set_timer(opps_timer,1500)


while True:

    for event in pygame.event.get(): # user action to quit
            if event.type == pygame.QUIT:
                pygame.quit() # opposite of pygame.init()
                exit() # ends rid of while true loop

            if game_active:
                if event.type == opps_timer:# and not pause_on:
                    opps.add(Opps(choice(['pink','blue','blue'])))

                if pause_on == False:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_shadow_rect.collidepoint(event.pos):
                            pause_on = True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_down_rect.collidepoint(event.pos):
                            pause_on = False
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    opps.empty()
                    player.sprite.rect.center = (320, 280)
                    score = 0
                    stamina_num = 6 # later, try to fix the stamina logic
                    stamina.empty()
                    health_num = 4
                    health.empty()
                    health.add(Health())
                    stamina.add(Stamina())


    if game_active:
        if pause_on:
            screen.blit(pause, (0,0))
            screen.blit(pause_down, pause_down_rect)

        else:
            screen.blit(bg, (0,0))
            score = display_score()

            screen.blit(pause_shadow, pause_shadow_rect)
            
            stamina.update()
            stamina.draw(screen)

            health.update()
            health.draw(screen)

            player.draw(screen)
            player.update()

            opps.update()
            opps.draw(screen)
            
            game_active = check_collision()

    else:
        screen.blit(start_screen, (0,0))

        score_message = font.render(f'Your score: {score}',False,'BLACK')
        score_message_rect = score_message.get_rect(center = (320,400))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)
