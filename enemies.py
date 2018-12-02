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


class enemy(spriteling.spriteling):
    def __init__(self, *args, **kwargs):
        super(enemy, self).__init__(*args, **kwargs)
        self.layer = config.enemy_layer

    def attack(self):
        pass

class simple_enemy(enemy):
    def __init__(self):
        super().__init__()
        self.velocity = (10, 0)

    def update(self, *args, **kwargs):
        self.rect.move_ip(self.velocity)
        super().update(*args, **kwargs)

class not_as_simple_enemies(enemy):
    def react(self, to, *args, **kwargs):
        if isinstance(to, blocks.block):
            self.velocity = (-self.velocity[0], -self.velocity[1])