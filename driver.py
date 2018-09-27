import pygame, config
pygame.init()

disp = pygame.display.set_mode(config.screen_size)
clock = pygame.time.Clock()

start_loop = True

while(start_loop):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        clock.tick(fps)
        print(clock.get_fps())