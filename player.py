import pygame
import spriteling
import overlays
from loader import player_img_loader

player_img_size =(38, 83)
img_boundary = (40, 85)
def calc_index(x_coord, y_coord):
    start_x = x_coord*img_boundary[0]+1
    start_y = y_coord*img_boundary[1]+1
    return pygame.rect.Rect((start_x, start_y), player_img_size)


goddess_robes     =  pygame.image.load('people\img_goddess1.png').convert_alpha()
goddess_crop_top  =  pygame.image.load('people\img_goddess2.png').convert_alpha()
goddess_body_suit =  pygame.image.load('people\img_goddess3.png').convert_alpha()
goddess_tattered  =  pygame.image.load('people\img_goddess4.png').convert_alpha()
img_lookup ={'robes': goddess_robes,
             'crop_top': goddess_crop_top,
             'body_suit': goddess_body_suit,
             'tattered': goddess_tattered
             }

#imgs = player_img_loader()

class player(spriteling.spriteling):
    def __init__(self, book, loc):

        super().__init__(image=img_lookup[book.goddess_lookup_key], loc=loc)

        self.spritesheet = img_lookup[book.goddess_lookup_key]
        self.string_lookup = {'topleft': calc_index(0, 0), 'neutral': calc_index(1, 1)}
        self.tuple_lookup = {(-1, -1):calc_index(0, 0), (0, 1): calc_index(1, 0), (1, -1): calc_index(2, 2),
                             (-1, 0): calc_index(0, 1), (0, 0): calc_index(1, 1), (1, 0): calc_index(2, 1),
                             (-1, 1): calc_index(0, 2), (0, -1): calc_index(1, 2), (1, 1): calc_index(2, 2)}
        self.image = self.spritesheet.subsurface(self.string_lookup['neutral'])

        self.hitboxes.add(spriteling.hitbox(self,
                                            scale_x=-(self.rect.height*0.2), scale_y=-(self.rect.width*0.2)))

        self.spell_slot = self.rect.center
        self.book = book

        self.active_spell = pygame.sprite.GroupSingle()

        self.move_mult = (4, 4)
        self.facing = (1, 0)
        self.prev_facing = (self.facing)

        self.missiles = pygame.sprite.Group()

        # stats and inventory
        self.hp = 1000

    def update(self, *args, **kwargs):
        super().update(*args)
        # all this stuff is supposed to handle moving the player, but it doesn't work right. It does handle facing, and
        # getting the right image, which is nice, but as of now all the movement is done by the move() method in
        # spriteling
        self.prev_facing = self.facing
        if 'move' in kwargs:
            print('moving', kwargs['move'])
            self.rect.move_ip(kwargs['move'])
        if 'look' in kwargs and any in kwargs['look'] != 0:
            self.facing = kwargs['look']
        elif 'move' in kwargs:
            if kwargs['move'][0] > 0.2:
                self.facing = (1, 0)
            elif kwargs['move'][0] < -0.2:
                self.facing = (-1, 0)
            elif kwargs['move'][1] > 0.2 and kwargs['move'][1] > abs(kwargs['move'][0]):
                self.facing = (0, -1)
            elif kwargs['move'][1] < -0.2 and abs(kwargs['move'][1]) > abs(kwargs['move'][0]):
                self.facing = (0, 1)
        else:
            self.facing = self.prev_facing

        self.image = self.spritesheet.subsurface(self.tuple_lookup[self.facing])


# a side/parallel class to player.
class multiplayer(player):
    def __init__(self, book):
        player.__init__(self, book, (0, 0))
        print("book level is: ", book.level, "book spells are: ", book.spells)
