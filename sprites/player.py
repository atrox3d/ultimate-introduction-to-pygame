from pathlib import Path
from types import SimpleNamespace

import pygame


class Player(pygame.sprite.Sprite):
    paths = SimpleNamespace()
    paths.IMAGES_PATH = Path('graphics/player')
    paths.WALK1 = paths.IMAGES_PATH / 'player_walk_1.png'
    paths.WALK2 = paths.IMAGES_PATH / 'player_walk_2.png'
    paths.JUMP = paths.IMAGES_PATH / 'jump.png'
    paths.STAND = paths.IMAGES_PATH / 'player_stand.png'

    paths.SOUNDS_PATH = Path('audio')
    paths.JUMP_SOUND = paths.SOUNDS_PATH / 'jump.mp3'

    LEFT = 80
    BOTTOM = 300
    MIDBOTTOM = LEFT, BOTTOM

    def __init__(self):
        super().__init__()

        self.images = SimpleNamespace()

        self.images.walk1 = pygame.image.load(self.paths.WALK1).convert_alpha()  # load player and convert respecting alpha channel
        self.images.walk2 = pygame.image.load(self.paths.WALK2).convert_alpha()  # load player and convert respecting alpha channel
        self.images.walk = [self.images.walk1, self.images.walk2]
        self.index = 0
        self.images.jump = pygame.image.load(self.paths.JUMP).convert_alpha()  # load player and convert respecting alpha channel

        self.images.stand = pygame.image.load(self.paths.STAND).convert_alpha()  # load player and convert respecting alpha channel

        self.image = self.images.walk[self.index]
        self.rect = self.image.get_rect(midbottom=Player.MIDBOTTOM)
        self.gravity = 0

        self.sounds = SimpleNamespace()
        self.sounds.jump = pygame.mixer.Sound(self.paths.JUMP_SOUND)
        self.sounds.jump.set_volume(0.5)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= Player.BOTTOM:
            self.jump()

    def jump(self):
        self.gravity = -20
        self.sounds.jump.play()

    def get_player_stand(self):
        stand = pygame.transform.rotozoom(self.images.stand, 0, 2)  # scale by 2 at angle 0
        stand_rect = stand.get_rect(center=(400, 200))  # get centered rect
        return stand, stand_rect

    def animation(self):
        if self.rect.bottom < self.BOTTOM:
            self.image = self.images.jump
        else:
            self.index += 0.1
            if self.index >= len(self.images.walk): self.index = 0
            self.image = self.images.walk[int(self.index)]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= Player.BOTTOM:
            self.rect.bottom = Player.BOTTOM

    def update(self):
        self.input()
        self.apply_gravity()
        self.animation()
