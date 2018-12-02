#
#                                                                .-`
#                                                                .-`
#                                                                 ``.`
#                                                 ..               `-.
#                             ``                  --               `-.
#           -/-               .-`                 ````             `-.          `//
#           :o+::::::::::::://--`                   .-`        :////+/:::::::::::oo
#             -sssshhdmmmmmmNN++.`                  .-`      ::mNNNNmmmmmmdhysss+
#                  syyyyyyhhhhdd/.`                 ..`      ddhhhhhhhyyyyyy:
#                  `````````````..`                   ..`    ```````````--``
#                                 `..                 .-`               ..`
#                                 `-.                 .-`                 ..`                       `.
# ......                          `-.                 .-`                 .-`                       `-
# -.`.oo......`                    ``......`          ```.`               .-.........               `-
# -. `::+o:---.``````               `-......````        `````             ``.--------               `-
# -.    yh/------....```````        `-..........````      `-.``             .--------               `-
# -.    yh/--...............`````````-..............```````--++.````````````.----++++.`             `-
# -.  --hh+/::::::::::::::::............................-////mm+//////////----:/+mmhh:-`            `-
# .. .hhmmmmmddddmmmmmmmmmmd----......................--oddmmmmmmmmmmmhdmm+:::smmdd----`            `-
# ....``dmmms///+mmmmmmmmmddmmdd/.....................sds/ommddmmmmmmh..mm/:::omh------`          `..-
# ..-.  hhmms:::/mmddmmmmy.-mm+/-.....................---:+mmhhmmmmmmmddmm-   /mh------..`        `---
# ..-.  yhmms:-`.mmddmmmmmhhmm.``.......................``-dd//dmmmmmmmmdd.  `/dh--------.        .---
# ..-.  yhmms:- .mm++hmmmmmmdd` `.......................` `--yyo+++++odd--` /so/:--------.      `..---
# ......--ydhy+ `::sso+++++odd.`........................```  ::sssssso::  +o+/:....------.      .---/o
# ....--  ohsoo+/``//ossssso++............................`````/+++++/````/+-......------.    ``--/o+/
# ....--  :/+++o+``../ooooo+.....................................................------.``    .-/+++/.
# ....--  ``+ho...........................................................-------------`      .-+o:...
# ....--  .-+hs------...-...............................................---------------`    ``........
# ....--  .-+hs-------------..........................................---------------..`   `..  `.....
# ....--  .-+hs-------------........................................-----------------    `-.  .-......

import pygame, spriteling, events, spells, config, blocks
from events import event_maker

skull_img = pygame.image.load(    'Animation\img_sun_particle.png').convert()
skull_img.set_colorkey(config.default_transparency)


class enemy(spriteling.spriteling):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = config.enemy_layer

    def attack(self):
        pass


class simple_enemy(enemy):
    def __init__(self):
        super().__init__()


    def update(self, *args, **kwargs):
        self.rect.move_ip(self.move(vel=(10, 0)))
        super().update(*args, **kwargs)



class patrol(simple_enemy):
    pass


class bouncy(simple_enemy):
    pass


class abenenoemy(enemy):
    def __init__(self, location):
        super().__init__(img=skull_img, loc=location)



class quintenemy(enemy):
    def __init__(self, location, patrol_route):
        super().__init__(loc=location)

        self.base_move = 4

        self.patrol_route = patrol_route
        self.stop = 0
        self.dest = self.patrol_route[self.stop]

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.rect.collidepoint(self.dest):
            self.stop += 1
            if self.stop >= len(self.patrol_route):
                self.stop = 0
            self.dest = self.patrol_route[self.stop]
        else:
            x_v, y_v = 0, 0
            if self.rect.centerx < self.dest[0]:
                x_v += 1
            elif self.rect.centerx > self.dest[0]:
                x_v -= 1
            if self.rect.centery < self.dest[1]:
                y_v += 1
            elif self.rect.centery > self.dest[1]:
                y_v -= 1
            # LOGAN:::DEBUG inefficient, will likely change
            self.move(True, move=(x_v, y_v))



class brain_storm():
    pass


class not_as_simple_enemies(enemy):
    # when this thing hits a wall
    def react(self, to, *args, **kwargs):
        if isinstance(to, blocks.block):
            self.velocity = (-self.velocity[0], -self.velocity[1])