import pygame
# https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
from sys import exit
from random import randint


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


def obstacle_movement(obstacle_list):
    """
    update every obstacle and remove it if off-screen

    list is passed by reference, so it is updated between calls

    :param obstacle_list:
    :return:
    """
    for obstacle_rect in obstacle_list:
        obstacle_rect.x -= 5
        if obstacle_rect.right < 0:
            obstacle_list.remove(obstacle_rect)

        if obstacle_rect.bottom == 300:
            screen.blit(snail, obstacle_rect)
        else:
            screen.blit(fly, obstacle_rect)
    # print(f'{len(obstacle_list) = }')


def collisions(player, obstacles):
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            return False
    return True


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
snail_img = 'graphics/snail/snail1.png'
snail = pygame.image.load(snail_img).convert_alpha()                # load snail and converting respecting alpha channel
# snail_rect = snail.get_rect(bottomright=(600, 300))
#
fly_img = 'graphics/Fly/Fly1.png'
fly = pygame.image.load(fly_img).convert_alpha()                    # load snail and converting respecting alpha channel
# fly_rect = fly.get_rect(bottomright=(600, 300))

obstacle_rect_list = []
#
player_img = 'graphics/Player/player_walk_1.png'
player = pygame.image.load(player_img).convert_alpha()              # load player and convert respecting alpha channel
# player_rect = pygame.rect(left, top, width, height)
player_rect = player.get_rect(midbottom=(80, 300))
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
                print('test timer')
                if randint(0, 1):
                    print('snail')
                    obstacle_rect_list.append(snail.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    print('fly')
                    obstacle_rect_list.append(fly.get_rect(bottomright=(randint(900, 1100), 210)))
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
        if player_gravity < 200: player_gravity += 1                # calc gravity acceleration
        player_rect.bottom += player_gravity                        # apply gravity to player, if jumping
        if player_rect.bottom >= 300: player_rect.bottom = 300      # stop at terrain
        screen.blit(player, player_rect)                            # draw player using rect
        #                                                           
        obstacle_movement(obstacle_rect_list)                       # update enemies on screen
        #                                                           
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
                                                                    
        # keys = pygame.key.get_pressed()                           # get state of ALL keys
        # if keys[pygame.K_SPACE]:                                  # check if space is True
        #     print('jump')

        # pygame.draw.line(screen, 'black', (0, 0), (screen.get_width(), screen.get_height()))
        # if player_rect.colliderect(snail_rect):
        #     print("COLLISION")

        # if player_rect.collidepoint(pygame.mouse.get_pos()):
        #     print("COLLISION")
        #     print(pygame.mouse.get_pressed())
        game_active = collisions(player_rect, obstacle_rect_list)   # check collisions, game over if true
        # update everything
    else:
        screen.fill((94, 129, 162))                                 # game over screen bg color
        screen.blit(player_stand, player_stand_rect)                # draw character and center it
        screen.blit(title, title_rect)                              # draw score

        player_rect.midbottom = (80, 300)                           # reset player position
        player_gravity = 0                                          # reset gravity
        obstacle_rect_list.clear()                                  # reset enemies

        # draw score or message
        if score:
            score_message = font.render(f'Your Score: {score}', False, (64, 64, 64))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)           # draw score
        else:
            screen.blit(game_message, game_message_rect)            # draw message

    pygame.display.update()                                         # update display surface
    clock.tick(60)                                                  # set framerate: 60fps/one loop every 1.666 milliseconds
