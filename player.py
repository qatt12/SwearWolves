import pygame
import spriteling
import config
import events
from events import event_maker
import overlays
from loader import player_img_loader

print("player.py has been imported")

player_img_size =(38, 83)
img_boundary = (40, 85)
def calc_index(x_coord, y_coord):
    start_x = x_coord*img_boundary[0]+1
    start_y = y_coord*img_boundary[1]+1
    return pygame.rect.Rect((start_x, start_y), player_img_size)


goddess_robes     =  pygame.image.load('Animation\img_goddess1.png').convert()
goddess_crop_top  =  pygame.image.load('Animation\img_goddess2.png').convert()
goddess_body_suit =  pygame.image.load('Animation\img_goddess3.png').convert()
goddess_tattered  =  pygame.image.load('Animation\img_goddess4.png').convert()
goddess_robes.set_colorkey(    config.default_transparency)
goddess_crop_top.set_colorkey( config.default_transparency)
goddess_body_suit.set_colorkey(config.default_transparency)
goddess_tattered.set_colorkey( config.default_transparency)

img_lookup = {'robes': goddess_robes,
              'crop_top': goddess_crop_top,
              'body_suit': goddess_body_suit,
              'tattered': goddess_tattered,
              }




class player(spriteling.spriteling):
    def __init__(self, book, loc, **kwargs):
        super().__init__(image=img_lookup[book.goddess_lookup_key], loc=loc)

        self.spritesheet = img_lookup[book.goddess_lookup_key]
        self.string_lookup = {'topleft': calc_index(0, 0), 'neutral': calc_index(1, 1)}
        self.tuple_lookup = {(-1, -1): calc_index(0, 0), (0, -1): calc_index(1, 0), (1, -1): calc_index(2, 0),
                             (-1, 0): calc_index(0, 1), (0, 0): calc_index(1, 1), (1, 0): calc_index(2, 1),
                             (-1, 1): calc_index(0, 2), (0, 1): calc_index(1, 2), (1, 1): calc_index(2, 2)}
        self.image = self.spritesheet.subsurface(self.string_lookup['neutral'])
        self.rect = self.image.get_rect()

        self.hitbox = spriteling.hitbox(self,
                                        scale_y=-(self.rect.height*0.3), scale_x=-(self.rect.width*0.2))
        self.layer = config.player_layer

        self.activity_state = {
            'interacting': False,
            'feet_locked': False,
            'aim_locked': False,
        }

        self.spell_slot = self.rect.center
        self.book = book

        self.active_spell = pygame.sprite.GroupSingle()

        self.base_move = 6
        self.curr_move = 6

        self.facing = (1, 0)
        self.facing_angle = spriteling.facing_angle(*self.facing)

        self.prev_facing = self.facing

        self.missiles = pygame.sprite.Group()

        # stats and inventory
        self.hp = 1000

    def update(self, *args, **kwargs):
        if self.curr_hp <= 0:
            self.kill()
            event_maker.new_event(events.player_event, 'player', subtype=events.player_died, dead_player=self)
        super().update(*args, **kwargs)
        # all this stuff is supposed to handle moving the player, but it doesn't work right. It does handle facing, and
        # getting the right image, which is nice, but as of now all the movement is done by the move() method in
        # spriteling
        #self.prev_facing = self.facing
        '''if 'look' in kwargs and any in kwargs['look'] != 0:
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
            self.facing = self.prev_facing'''

        # ********** DEBUG STUFF
        if 'stick_data' in kwargs:
            x_move_input, y_move_input = kwargs['stick_data']['move'][0], kwargs['stick_data']['move'][1]
            mod_facing, lock_facing = kwargs['stick_data']['mod_look'], kwargs['stick_data']['lock_look']
            x_look_input, y_look_input = kwargs['stick_data']['look'][0], kwargs['stick_data']['look'][1]
            self.facing = self.facing_angle(x_move_input, y_move_input, mod_facing, lock_facing)

        if 'interact' in kwargs:
            if kwargs['interact'][0] >= kwargs['interact'][1] >= 1:

                self.activity_state['interacting'] = True
            else:
                self.activity_state['interacting'] = False

        self.image = self.spritesheet.subsurface(self.tuple_lookup[self.facing])

# a side/parallel class to player.
class multiplayer(player):
    def __init__(self, book, number):
        player.__init__(self, book,  (0, 0))
        print("book level is: ", book.level, "book spells are: ", book.spells)
        self.number = number

