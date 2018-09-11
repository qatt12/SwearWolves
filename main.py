#main is the primary driver file that controls the game loop and makes calls to the dungeon and room classes/instances
#this keeps everything in order, controls the menu state, etc.

import pygame, config, random

pygame.init()

disp = pygame.display.set_mode(config.screen_size)
clock = pygame.time.Clock()

import room, player, spells

r_x = random.randint(4, 20)
r_y = random.randint(4, 20)
print("x = ", r_x, "y = ", r_y)

current_room = room.room((r_x, r_y), room.theme())

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass

        clock.tick(config.fps)
        current_room.draw_contents(disp)
        current_room.draw_boxes(disp)

        pygame.display.update()
        pygame.display.flip()


        pygame.event.pump()
