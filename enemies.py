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

import pygame, spriteling, events, spells, config
from events import event_maker

class charged_attack(spriteling.spriteling):
    def __init__(self, time):
        super().__init__()
        self.cooldown = time * config.fps
        self.timer = 0

    def update(self, fire, missile_layer, *args, **kwargs):
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0 and fire:
            pass


class enemy(spriteling.spriteling):
    def __init__(self, *args, **kwargs):
        super(enemy, self).__init__(*args, **kwargs)
        self.layer = config.enemy_layer

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

class simple_enemy(enemy):
    def __init__(self):
        super().__init__()
        #self.attack = spells.fireball_s()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        #self.attack.update(True, self.rect.center, True, True, (1, 0))
