import random
from pathlib import Path

import pygame


class Obstacle(pygame.sprite.Sprite):
    FLY = 'fly'.lower()
    SNAIL = 'snail'.lower()

    FLY_IMAGES_PATH = Path('graphics/Fly')
    FLY1 = FLY_IMAGES_PATH / 'Fly1.png'
    FLY2 = FLY_IMAGES_PATH / 'Fly2.png'

    SNAIL_IMAGES_PATH = Path('graphics/snail')
    SNAIL1 = SNAIL_IMAGES_PATH / 'snail1.png'
    SNAIL2 = SNAIL_IMAGES_PATH / 'snail2.png'

    def __init__(self, type):
        super().__init__()

        self.type = type.lower()
        self.y_pos = 0

        if self.type == self.FLY:
            fly1 = pygame.image.load(self.FLY1).convert_alpha()
            fly2 = pygame.image.load(self.FLY2).convert_alpha()
            self.frames = [fly1, fly2]
            self.y_pos = 210
        elif self.type == self.SNAIL:
            snail1 = pygame.image.load(self.SNAIL1).convert_alpha()
            snail2 = pygame.image.load(self.SNAIL2).convert_alpha()
            self.frames = [snail1, snail2]
            self.y_pos = 300
        else:
            raise TypeError(f'Unknown obstacle type: {self.type}')

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), self.y_pos))

    def animation(self):
        self.index += 0.1
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
