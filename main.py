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
text = font.render(
                    game_title,                             # text to draw
                    False,                                  # antialiasing,
                    'black'                                 # color
)
#
sky_img = 'graphics/Sky.png'
sky_bg = pygame.image.load(sky_img).convert()               # load sky background and convert it
ground_img = 'graphics/ground.png'
ground_bg = pygame.image.load(ground_img).convert()         # load terrain background and convert it
#
snail_img = 'graphics/snail/snail1.png'
snail = pygame.image.load(snail_img).convert_alpha()        # load snail and converting respecting alpha channel
snail_x = 600
#
player_img = 'graphics/Player/player_walk_1.png'
player = pygame.image.load(player_img).convert_alpha()      # load player and convert respecting alpha channel
# player_rect = pygame.rect(left, top, width, height)
player_rect = player.get_rect(midbottom=(80, 300))

while True:                                                 # main loop
    for event in pygame.event.get():                        # loop through events
        if event.type == pygame.QUIT:                       # quit by closing window
            pygame.quit()
            exit()                                          # prevent further updates

    # draw all our elements

    # when drawing surfaces order is relevant
    # latest are topmost, this rectangle is hidden!
    screen.blit(rectangle_surface, (200, 100))              # draw rectangle on screen
    #
    screen.blit(sky_bg, (0, 0))                             # draw sky
    screen.blit(ground_bg, (0, 300))                        # draw terrain
    #
    screen.blit(text, (300, 50))                            # draw text
    #
    screen.blit(snail, (snail_x, 250))                      # draw snail
    snail_x = snail_x < -100 and 800 or snail_x - 4         # update snail position
    #
    screen.blit(player, player_rect)                        # draw player using rect
    # update everything
    pygame.display.update()                                 # update display surface
    clock.tick(60)                                          # set framerate: 60fps/one loop every 1.666 milliseconds
