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

import pygame, spriteling

class enemy(spriteling.spriteling):
    def __init__(self, *args, **kwargs):
        super(enemy, self).__init__(*args, **kwargs)