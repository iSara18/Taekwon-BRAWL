import pygame
import os, sys


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