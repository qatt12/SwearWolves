import pygame
import spriteling
from loader import player_img_loader

player_img_size =(38, 83)
img_boundary = (40, 85)
def calc_index(x_coord, y_coord):
    if x_coord == 0:
        x = 1
    if y_coord == 0:
        y = 1

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
        self.string_lookup = {'neutral': ((41, 86), (38, 83))}
        self.tuple_lookup = {(0, 0): ((41, 86), (38, 83))}
        self.image = self.spritesheet.subsurface(self.string_lookup['neutral'])

        self.hitboxes.add(spriteling.hitbox(self,
                                            scale_x=-(self.rect.height*0.2), scale_y=-(self.rect.width*0.2)))

        self.spell_slot = self.rect.center
        self.book = book

        self.active_spell = pygame.sprite.GroupSingle()

        self.move_mult = (4, 4)

    def update(self, *args, **kwargs):
        super().update(*args)
        self.image = self.spritesheet.subsurface(self.string_lookup['neutral'])




# a side/parallel class to player.
class multiplayer(player):
    def __init__(self, book):
        player.__init__(self, book, (0, 0))
        print("book level is: ", book.level, "book spells are: ", book.spells)
        #self.active_spell = book.spells[book.index]


