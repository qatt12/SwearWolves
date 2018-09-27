#main is the primary driver file that controls the game loop and makes calls to the dungeon and room classes/instances
#this keeps everything in order, controls the menu state, etc.

import pygame, config, random, controllers

from config import fps as fps
pygame.init()

disp = pygame.display.set_mode(config.screen_size)
clock = pygame.time.Clock()

# creates/inits/prepares all attached joysticks/controllers/gamepads
all_controllers = [controllers.auto_assign(each) for each in controllers.prepare_joysticks()]

import room, player, spells

r_x = random.randint(4, 7)
r_y = random.randint(4, 7)
print("x = ", r_x, "y = ", r_y)

current_room = room.room((r_x, r_y), room.theme())
input_devices = [controllers.interface(each) for each in all_controllers]
print("detected input devices: ", len(input_devices))

players = pygame.sprite.Group()

for each in input_devices:
    if each.controller.pull_button(each.accept):
        players.add(player.player(each, (0, 0)))

current_room.add_players(players)

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        clock.tick(fps)
        print(clock.get_fps())


        current_room.update()

        current_room.draw_contents(disp)
        current_room.draw_boxes(disp)

        pygame.display.update()
        #pygame.display.flip()

        pygame.event.pump()
        pygame.time.wait(0)
