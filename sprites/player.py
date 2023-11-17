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

        player_walk1 = pygame.image.load(self.WALK1).convert_alpha()  # load player and convert respecting alpha channel
        player_walk2 = pygame.image.load(self.WALK2).convert_alpha()  # load player and convert respecting alpha channel
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load(self.JUMP).convert_alpha()  # load player and convert respecting alpha channel

        self.player_stand = pygame.image.load(self.STAND).convert_alpha()  # load player and convert respecting alpha channel

        self.image = self.player_walk[self.player_index]
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
        player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)  # scale by 2 at angle 0
        player_stand_rect = player_stand.get_rect(center=(400, 200))  # get centered rect
        return player_stand, player_stand_rect

    def animation(self):
        if self.rect.bottom < self.BOTTOM:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= Player.BOTTOM:
            self.rect.bottom = Player.BOTTOM

    def update(self):
        self.input()
        self.apply_gravity()
        self.animation()
