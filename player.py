import pygame, spells
import spriteling


spritesheet = pygame.image.load('people\smol_silvia.png').convert_alpha()
neutral = spritesheet.subsurface((0,0), (59,126))
right = spritesheet.subsurface((60,0), (67,126))
top_right = spritesheet.subsurface((128, 0), (58, 126))
bottom_right = spritesheet.subsurface((187,0), (67,126))
left = pygame.transform.flip(right, 1, 0)
top_left = pygame.transform.flip(top_right, 1, 0)
bottom_left = pygame.transform.flip(bottom_right, 1, 0)
down = spritesheet.subsurface((257, 0), (38, 126))
top = spritesheet.subsurface((299, 0), (38, 126))

class menu_player_one(pygame.sprite.Sprite):
    pass

class menu_player():
    pass

class player(spriteling.spriteling):
    def __init__(self, input_device, loc):
        super().__init__(image=neutral, loc=loc)

        # the following is testing code, copy-pasted from the earlier project so that I can get a testable instance of
        # the game running
        self.torso = {(0, 0): neutral, (1, 0): right, (1, -1): top_right, (1, 1): bottom_right, (0, -1): top,
                      (0, 1): down, (-1, 0): left, (-1, -1): top_left, (-1, 1): bottom_left}

        self.hitboxes.add(spriteling.hitbox(self,
                                            scale_x=-(self.rect.height*0.2), scale_y=-(self.rect.width*0.2)))
        self.vel = (0, 0)
        self.max_vel = 4
        self.facing = (0, 0)
        # end of testing code

        # All of this stuff here will have to be fixed
        self.book_slot = (0, 0)
        self.spell_slot = self.rect.center
        self.book = spells.DEBUG_book(self)

        self.active_spell = pygame.sprite.GroupSingle(self.book.get_spell(input_device))
        self.active_missiles = pygame.sprite.Group()

        # attaches the interface to the player
        self.input_device = input_device

    def update(self, *args):
        # its crucial to always update the input
        self.input_device.update()
        self.vel = (int(self.input_device.moving[0] * self.max_vel), int(self.input_device.moving[1] * self.max_vel))
        self.rect.move_ip(self.vel)
        self.hitboxes.update()
        self.active_spell.update(self.rect.center, self.input_device, self.active_missiles)

    def get_live_missiles(self):
        return self.active_missiles


class multiplayer(player):
    def __init__(self, input_dev, book, num):
        super().__init__(input_dev, (0, 0))
        self.book = book


