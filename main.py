import pygame
# https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used
from sys import exit

pygame.init()                                           # initialize engine

width = 800
height = 400
screen = pygame.display.set_mode((width, height))       # create display surface
game_title = 'Runner'
pygame.display.set_caption(game_title)                  # set window title

clock = pygame.time.Clock()                             # instantiate clock object

rectangle_surface = pygame.Surface((100, 200))          # create rectangle 100*200 (w, h)
rectangle_surface.fill('red')                           # fill rectangle with red
#
font = pygame.font.Font(
                        # None,                           # None = default font
                        'font/Pixeltype.ttf',           # load font
                        50                              # font size
)
text = font.render(
                    game_title,                         # text to draw
                    False,                              # antialiasing,
                    'black'                             # color
)
#
sky_bg = pygame.image.load('graphics/Sky.png')          # load sky background
ground_bg = pygame.image.load('graphics/ground.png')    # load terrain background
#
snail = pygame.image.load('graphics/snail/snail1.png')
snail_x = 600

while True:                                             # main loop
    for event in pygame.event.get():                    # loop through events
        if event.type == pygame.QUIT:                   # quit by closing window
            pygame.quit()
            exit()                                      # prevent further updates

    # draw all our elements

    # when drawing surfaces order is relevant
    # latest are topmost, this rectangle is hidden!
    screen.blit(rectangle_surface, (200, 100))          # draw rectangle on screen
    #
    screen.blit(sky_bg, (0, 0))                         # draw sky
    screen.blit(ground_bg, (0, 300))                    # draw terrain
    #
    screen.blit(text, (300, 50))                        # draw text
    #
    screen.blit(snail, (snail_x, 250))                  # draw snail
    snail_x = snail_x < -100 and 800 or snail_x - 4     # update snail position

    # update everything
    pygame.display.update()                             # update display surface
    clock.tick(60)                                      # set framerate: 60fps/one loop every 1.666 milliseconds
