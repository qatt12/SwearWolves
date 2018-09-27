import pygame, config
from misc import controller_list as c_list
pygame.init()

disp = pygame.display.set_mode(config.screen_size)
clock = pygame.time.Clock()

start_loop = True
player_select_loop = True
import interface

cntrllr = c_list()
player_one = None

while(start_loop):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # clock.tick(config.fps)
        print(clock.get_fps())

        if cntrllr.is_p1_ready():
            player_one = cntrllr.get_p1()
            start_loop = False

        cntrllr.update()

        pygame.display.update()

        pygame.event.pump()
        pygame.time.wait(0)

