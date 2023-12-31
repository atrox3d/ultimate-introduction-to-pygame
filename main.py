import random
from pathlib import Path

import pygame
# https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
from sys import exit

from sprites.obstacle import Obstacle
from sprites.player import Player


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
    screen.blit(score, score_rect)                          # draw score
    return current_time


pygame.init()                                                       # initialize engine
#
# game window
#
width = 800
height = 400
screen = pygame.display.set_mode((width, height))                   # create display surface
game_title = 'Pixel Runner'
pygame.display.set_caption(game_title)                              # set window title
#
# game params
#
game_active = False
start_time = 0
score = 0
clock = pygame.time.Clock()                                         # instantiate clock object
#
# game music
#
bg_music = pygame.mixer.Sound(Path('audio/music.wav'))
bg_music.set_volume(0.8)
bg_music.play(loops=-1)
#
# player
#
player = pygame.sprite.GroupSingle()
player.add(Player())
#
# obstacles
#
obstacles = pygame.sprite.Group()
#
# game bg
#
sky_img = 'graphics/Sky.png'
sky_bg = pygame.image.load(sky_img).convert()                       # load sky background and convert it
#
ground_img = 'graphics/ground.png'
ground_bg = pygame.image.load(ground_img).convert()                 # load terrain background and convert it
#
# game title, message
#
font = pygame.font.Font(
                        # None,                                       # None = default font
                        'font/Pixeltype.ttf',                       # load font
                        50                                          # font size
)
#
title = font.render(game_title, False, (64, 64, 64))
title_rect = title.get_rect(center=(400, 50))                       # get centered rect from text
#
game_message = font.render('Press SPACE to Run', False, (64, 64, 64))
game_message_rect = game_message.get_rect(center=(400, 350))
#
# game timers
#
obstacle_timer = pygame.USEREVENT + 1                               # get next user event available
pygame.time.set_timer(obstacle_timer, 900)                          # set user event every 900 ms
#
#
# main loop
#
#
while True:                                                         # main loop
    #
    # event loop
    #
    for event in pygame.event.get():                                # loop through events
        #
        # quit, anywhere in the game
        #
        if event.type == pygame.QUIT:                               # quit by closing window
            pygame.quit()
            exit()                                                  # prevent further updates
        if event.type == pygame.KEYDOWN:                            # check if key is pressed
            if event.key == pygame.K_q:                             # if pressed check if q
                pygame.quit()
                exit()
        #
        # events depending on game state
        #
        if game_active:
            if event.type == pygame.KEYDOWN:                        # check if key is pressed
                if event.key == pygame.K_q:                       # if pressed check if q
                    pygame.quit()
                    exit()
            elif event.type == obstacle_timer:
                obstacle_type = random.choice([Obstacle.FLY, Obstacle.SNAIL, Obstacle.SNAIL, Obstacle.SNAIL])
                obstacles.add(Obstacle(obstacle_type))
        else:
            if event.type == pygame.KEYDOWN:                        # check if key is pressed
                if event.key == pygame.K_SPACE:                     # if pressed check if space
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
    #
    # screen update depending on game state
    #
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

        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        game_active = sprite_collision()
        # update everything
    else:
        screen.fill((94, 129, 162))                                 # game over screen bg color
        screen.blit(*player.sprite.get_player_stand())                # draw character and center it
        screen.blit(title, title_rect)                              # draw score

        # draw score or message
        if score:
            score_message = font.render(f'Your Score: {score}', False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)           # draw score
        else:
            screen.blit(game_message, game_message_rect)            # draw message

    pygame.display.update()                                         # update display surface
    clock.tick(60)                                                  # set framerate: 60fps/one loop every 1.666 milliseconds
