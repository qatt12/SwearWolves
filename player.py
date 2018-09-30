import pygame
import spriteling

goddess_robes     =  pygame.image.load('people\img_goddess1.png').convert_alpha()
goddess_crop_top  =  pygame.image.load('people\img_goddess2.png').convert_alpha()
goddess_body_suit =  pygame.image.load('people\img_goddess3.png').convert_alpha()
goddess_tattered  =  pygame.image.load('people\img_goddess4.png').convert_alpha()
img_lookup ={'robes': goddess_robes,
             'crop_top': goddess_crop_top,
             'body_suit': goddess_body_suit,
             'tattered': goddess_tattered
             }


class player(spriteling.spriteling):
    def __init__(self, book, loc):

        super().__init__(image=img_lookup[book.goddess_lookup_key], loc=loc)

        self.hitboxes.add(spriteling.hitbox(self,
                                            scale_x=-(self.rect.height*0.2), scale_y=-(self.rect.width*0.2)))

        self.spell_slot = self.rect.center
        self.book = book

        self.active_missiles = pygame.sprite.GroupSingle()

    def update(self, *args):
        pass

# a side/parallel class to player.
class multiplayer(spriteling.spriteling):
    def __init__(self, plyr_img, actv_spell):
        super().__init__(image=plyr_img, loc=(0, 0))
        self.active_spell = actv_spell


