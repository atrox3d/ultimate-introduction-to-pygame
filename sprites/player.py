from pathlib import Path

import pygame


class Player(pygame.sprite.Sprite):
    IMAGES_PATH = Path('graphics/player')
    WALK1 = IMAGES_PATH / 'player_walk_1.png'
    WALK2 = IMAGES_PATH / 'player_walk_2.png'
    JUMP = IMAGES_PATH / 'jump.png'
    STAND = IMAGES_PATH / 'player_stand.png'

    SOUNDS_PATH = Path('audio')
    JUMP_SOUND = SOUNDS_PATH / 'jump.mp3'

    LEFT = 80
    BOTTOM = 300
    MIDBOTTOM = LEFT, BOTTOM

    def __init__(self):
        super().__init__()

        walk1 = pygame.image.load(self.WALK1).convert_alpha()  # load player and convert respecting alpha channel
        walk2 = pygame.image.load(self.WALK2).convert_alpha()  # load player and convert respecting alpha channel
        self.walk = [walk1, walk2]
        self.index = 0
        self.jump = pygame.image.load(self.JUMP).convert_alpha()  # load player and convert respecting alpha channel

        self.stand = pygame.image.load(self.STAND).convert_alpha()  # load player and convert respecting alpha channel

        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom=Player.MIDBOTTOM)
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound(self.JUMP_SOUND)
        self.jump_sound.set_volume(0.5)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= Player.BOTTOM:
            # TODO: create Player.jump()
            self.gravity = -20
            self.jump_sound.play()

    def get_player_stand(self):
        stand = pygame.transform.rotozoom(self.stand, 0, 2)  # scale by 2 at angle 0
        stand_rect = stand.get_rect(center=(400, 200))  # get centered rect
        return stand, stand_rect

    def animation(self):
        if self.rect.bottom < self.BOTTOM:
            self.image = self.jump
        else:
            self.index += 0.1
            if self.index >= len(self.walk): self.index = 0
            self.image = self.walk[int(self.index)]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= Player.BOTTOM:
            self.rect.bottom = Player.BOTTOM

    def update(self):
        self.input()
        self.apply_gravity()
        self.animation()
