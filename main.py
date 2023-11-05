import pygame
from sys import exit

pygame.init()                                           # initialize engine

width = 800
height = 400
screen = pygame.display.set_mode((width, height))       # create display surface

while True:                                             # main loop
    for event in pygame.event.get():                    # loop through events
        if event.type == pygame.QUIT:                   # quit by closing window
            pygame.quit()
            exit()                                      # prevent further updates
    # draw all our elements
    # update everything
    pygame.display.update()                             # update display surface

