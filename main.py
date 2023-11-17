import random
from pathlib import Path

import pygame
# https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    IMAGES_PATH = Path('graphics/player')
    WALK1 = IMAGES_PATH / 'player_walk_1.png'
    WALK2 = IMAGES_PATH / 'player_walk_2.png'
    JUMP = IMAGES_PATH / 'jump.png'

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


def sprite_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    else:
        return True


def display_score():
    """
    calculate and display game score
    :return:
    """
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    score = font.render(
        f'Score: {current_time}',  # text to draw
        False,  # antialiasing,
        # 'black'                                 # color
        (64, 64, 64)
    )
    score_rect = score.get_rect(center=(400, 50))  # get centered rect from text

    # score_bg = score_rect.inflate(15, 15)
    # # pygame.draw.rect(screen, 'Pink', score_bg)
    # pygame.draw.rect(screen, '#c0e8ec', score_bg, border_radius=10)
    screen.blit(score, score_rect)                          # draw score
    return current_time


def collisions(player, obstacles):
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            return False
    return True


def player_animation():
    """
    display walking animation if player on floor
    display jump if player in air

    :return:
    """
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()                                                       # initialize engine
width = 800
height = 400
screen = pygame.display.set_mode((width, height))                   # create display surface
game_title = 'Pixel Runner'
pygame.display.set_caption(game_title)                              # set window title

game_active = False
start_time = 0
score = 0
clock = pygame.time.Clock()                                         # instantiate clock object
bg_music = pygame.mixer.Sound(Path('audio/music.wav'))
bg_music.set_volume(0.8)
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()


rectangle_surface = pygame.Surface((100, 200))                      # create rectangle 100*200 (w, h)
rectangle_surface.fill('red')                                       # fill rectangle with red
#
font = pygame.font.Font(
                        # None,                                       # None = default font
                        'font/Pixeltype.ttf',                       # load font
                        50                                          # font size
)
#
sky_img = 'graphics/Sky.png'
sky_bg = pygame.image.load(sky_img).convert()                       # load sky background and convert it
#
ground_img = 'graphics/ground.png'
ground_bg = pygame.image.load(ground_img).convert()                 # load terrain background and convert it
#
player_walk1 = 'graphics/Player/player_walk_1.png'
player_walk1 = pygame.image.load(player_walk1).convert_alpha()      # load player and convert respecting alpha channel
player_walk2 = 'graphics/Player/player_walk_2.png'
player_walk2 = pygame.image.load(player_walk2).convert_alpha()      # load player and convert respecting alpha channel
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = 'graphics/Player/jump.png'
player_jump = pygame.image.load(player_jump).convert_alpha()        # load player and convert respecting alpha channel

# player_rect = pygame.rect(left, top, width, height)
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
#
player_stand = pygame.image.load('graphics/Player/player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)        # scale by 2 at angle 0
player_stand_rect = player_stand.get_rect(center=(400, 200))        # get centered rect
#
title = font.render(game_title, False, (64, 64, 64))
title_rect = title.get_rect(center=(400, 50))                       # get centered rect from text
#
game_message = font.render('Press SPACE to Run', False, (64, 64, 64))
game_message_rect = game_message.get_rect(center=(400, 350))
#
obstacle_timer = pygame.USEREVENT + 1                               # get next user event available
pygame.time.set_timer(obstacle_timer, 900)                          # set user event every 900 ms
#
snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)                          # set user event every 900 ms
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)                          # set user event every 900 ms

while True:                                                         # main loop
    for event in pygame.event.get():                                # loop through events
        if event.type == pygame.QUIT:                               # quit by closing window
            pygame.quit()
            exit()                                                  # prevent further updates
        if event.type == pygame.KEYDOWN:                            # check if key is pressed
            if event.key == pygame.K_q:                             # if pressed check if q
                pygame.quit()
                exit()

        if game_active:
            if event.type == pygame.KEYDOWN:                        # check if key is pressed
                if event.key == pygame.K_SPACE:                     # if pressed check if space
                    if player_rect.bottom >= 300:
                        print('jump')
                        player_gravity = -20                        # jump
                elif event.key == pygame.K_q:                       # if pressed check if q
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYUP:                        # check if key is released
                print('key up')
            elif event.type == pygame.MOUSEBUTTONDOWN:              # check if mouse button is pressed
                if player_rect.collidepoint(event.pos):             # check if mouse collides with player rect
                    if player_rect.bottom == 300:
                        print('jump')
                        player_gravity = -20                        # jump
            elif event.type == obstacle_timer:
                obstacle_type = random.choice([Obstacle.FLY, Obstacle.SNAIL, Obstacle.SNAIL, Obstacle.SNAIL])
                obstacles.add(Obstacle(obstacle_type))
                # print('OBSTACLE TIMER')
                # if randint(0, 1):
                #     obstacle_rect_list.append(snail.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     print('fly')
                #     obstacle_rect_list.append(fly.get_rect(bottomright=(randint(900, 1100), 210)))
        else:
            if event.type == pygame.KEYDOWN:                        # check if key is pressed
                if event.key == pygame.K_SPACE:                     # if pressed check if space
                    game_active = True
                    # snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # draw all our elements

        # when drawing surfaces order is relevant
        # latest are topmost, this rectangle is hidden!
        # screen.blit(rectangle_surface, (200, 100))                  # draw rectangle on screen
        #                                                           
        screen.blit(sky_bg, (0, 0))                                 # draw sky
        screen.blit(ground_bg, (0, 300))                            # draw terrain
        #                                                           
        score = display_score()                                     # update ad draw score
        #                                                           
        # if snail_rect.right <= 0:                                 # update snail position
        #     snail_rect.left = 800                                 
        # else:                                                     
        #     snail_rect.left -= 4                                  
        # screen.blit(snail, snail_rect)                            # draw snail using rect
        #                                                           
        # if player_gravity < 200: player_gravity += 1                # calc gravity acceleration
        # player_rect.bottom += player_gravity                        # apply gravity to player, if jumping
        # if player_rect.bottom >= 300: player_rect.bottom = 300      # stop at terrain
        # player_animation()
        # screen.blit(player_surf, player_rect)                            # draw player using rect

        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        game_active = sprite_collision()
        # game_active = collisions(player_rect, obstacle_rect_list)   # check collisions, game over if true
        # update everything
    else:
        screen.fill((94, 129, 162))                                 # game over screen bg color
        screen.blit(player_stand, player_stand_rect)                # draw character and center it
        screen.blit(title, title_rect)                              # draw score

        player_rect.midbottom = (80, 300)                           # reset player position
        player_gravity = 0                                          # reset gravity
        # obstacle_rect_list.clear()                                  # reset enemies

        # draw score or message
        if score:
            score_message = font.render(f'Your Score: {score}', False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)           # draw score
        else:
            screen.blit(game_message, game_message_rect)            # draw message

    pygame.display.update()                                         # update display surface
    clock.tick(60)                                                  # set framerate: 60fps/one loop every 1.666 milliseconds
