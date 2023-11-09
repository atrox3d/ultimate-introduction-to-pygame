import pygame
# https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
from sys import exit

pygame.init()                                               # initialize engine

width = 800
height = 400
screen = pygame.display.set_mode((width, height))           # create display surface
game_title = 'Runner'
pygame.display.set_caption(game_title)                      # set window title

clock = pygame.time.Clock()                                 # instantiate clock object

rectangle_surface = pygame.Surface((100, 200))              # create rectangle 100*200 (w, h)
rectangle_surface.fill('red')                               # fill rectangle with red
#
font = pygame.font.Font(
                        # None,                               # None = default font
                        'font/Pixeltype.ttf',               # load font
                        50                                  # font size
)
score = font.render(
                    game_title,                             # text to draw
                    False,                                  # antialiasing,
                    # 'black'                                 # color
                    (64, 64, 64)
)
score_rect = score.get_rect(center=(400, 50))               # get centered rect from text
#
sky_img = 'graphics/Sky.png'
sky_bg = pygame.image.load(sky_img).convert()               # load sky background and convert it
ground_img = 'graphics/ground.png'
ground_bg = pygame.image.load(ground_img).convert()         # load terrain background and convert it
#
snail_img = 'graphics/snail/snail1.png'
snail = pygame.image.load(snail_img).convert_alpha()        # load snail and converting respecting alpha channel
snail_rect = snail.get_rect(bottomright=(600, 300))
#
player_img = 'graphics/Player/player_walk_1.png'
player = pygame.image.load(player_img).convert_alpha()      # load player and convert respecting alpha channel
# player_rect = pygame.rect(left, top, width, height)
player_rect = player.get_rect(midbottom=(80, 300))
player_gravity = 0

while True:                                                 # main loop
    for event in pygame.event.get():                        # loop through events
        if event.type == pygame.QUIT:                       # quit by closing window
            pygame.quit()
            exit()                                          # prevent further updates
        elif event.type == pygame.KEYDOWN:                  # check if key is pressed
            print('key down')
            if event.key == pygame.K_SPACE:                 # if pressed check if space
                print('jump')
                player_gravity = -20                        # jump
            elif event.key == pygame.K_q:                   # if pressed check if q
                pygame.quit()
                exit()
        elif event.type == pygame.KEYUP:                    # check if key is released
            print('key up')
        elif event.type == pygame.MOUSEBUTTONDOWN:         # check if mouse button is pressed
            if player_rect.collidepoint(event.pos):        # check if mouse collides with player rect
                print('mouse collision')
                player_gravity = -20                        # jump

    # draw all our elements

    # when drawing surfaces order is relevant
    # latest are topmost, this rectangle is hidden!
    screen.blit(rectangle_surface, (200, 100))              # draw rectangle on screen
    #
    screen.blit(sky_bg, (0, 0))                             # draw sky
    screen.blit(ground_bg, (0, 300))                        # draw terrain
    #
    score_bg = score_rect.inflate(15, 15)
    # pygame.draw.rect(screen, 'Pink', score_bg)
    pygame.draw.rect(screen, '#c0e8ec', score_bg, border_radius=10)
    screen.blit(score, score_rect)                          # draw score
    #
    screen.blit(snail, snail_rect)                          # draw snail using rect
    if snail_rect.right <= 0:                               # update snail position
        snail_rect.left = 800
    else:
        snail_rect.left -= 4
    #
    if player_gravity < 200: player_gravity += 1
    player_rect.bottom += player_gravity
    if player_rect.bottom >= 300: player_rect.bottom = 300
    screen.blit(player, player_rect)                        # draw player using rect
    print(f'{player_gravity = }')

    # keys = pygame.key.get_pressed()                        # get state of ALL keys
    # if keys[pygame.K_SPACE]:                               # check if space is True
    #     print('jump')

    # pygame.draw.line(screen, 'black', (0, 0), (screen.get_width(), screen.get_height()))
    # if player_rect.colliderect(snail_rect):
    #     print("COLLISION")

    # if player_rect.collidepoint(pygame.mouse.get_pos()):
    #     print("COLLISION")
    #     print(pygame.mouse.get_pressed())

    # update everything
    pygame.display.update()                                 # update display surface
    clock.tick(60)                                          # set framerate: 60fps/one loop every 1.666 milliseconds
