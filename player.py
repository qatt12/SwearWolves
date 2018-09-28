import pygame
import spriteling

goddess = pygame.image.load('Animation\goddess3.png').convert_alpha()
neutral = goddess.subsurface((37, 85), (39, 84))

class menu_player_one(pygame.sprite.Sprite):
    pass

class menu_player():
    pass

class player(spriteling.spriteling):
    def __init__(self, book, loc):
        super().__init__(image=neutral, loc=loc)

        self.hitboxes.add(spriteling.hitbox(self,
                                            scale_x=-(self.rect.height*0.2), scale_y=-(self.rect.width*0.2)))
        self.vel = (0, 0)
        self.max_vel = 4
        self.facing = (0, 0)
        # end of testing code

        # All of this stuff here will have to be fixed
        self.book_slot = (0, 0)
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


