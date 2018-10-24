import pygame, spriteling, config
from config import hud_width_proportion as width_scalar
from config import hud_height_proportion as height_scalar

class hud(spriteling.spriteling):
    def __init__(self, player, book, player_num, *args, **kwargs):
        hud_width = int(config.screen_size[0] / width_scalar)
        hud_height = int(config.screen_size[1] / height_scalar)
        print("hud width= ", hud_width, "hud height= ", hud_height)
        # super().__init__(image=pygame.Surface((hud_width, hud_height)))
        super().__init__()
        self.rect = pygame.rect.Rect((0, 0), (hud_width, hud_height))
        if player_num == 2:
            self.rect.move_ip((width_scalar-1)*hud_width, 0)
        elif player_num == 3:
            self.rect.move_ip(0, (height_scalar-1)*hud_height)
        elif player_num == 4:
            self.rect.move_ip((width_scalar-1)*hud_width, (height_scalar-1)*hud_height)

        self.portrait = player.image
        self.portrait_slot = player.rect.clamp(self.rect)
        self.book_ref = book
        self.book_image = book.image
        self.book_slot = book.rect.clamp(self.rect)
        self.book_slot.left = self.portrait_slot.right

        if 'starting_xp' in kwargs:
            self.xp = kwargs['starting_xp']
        else:
            self.xp = 0
        if 'starting_potions' in kwargs:
            self.heal_potions = kwargs['starting_potions']
        else:
            self.heal_potions = 3
        self.boss_keys = 0
        self.keys = 1
        self.hp = player.hp
        self.ankhs = 1
        self.current_spell_index = book.get_active_spell()[0]
        self.spell_list = book.spells

        self.active_spell_slot = self.spell_list[0].rect.clamp(self.rect)
        self.active_spell_slot.left = self.portrait_slot.right
        self.active_spell_slot.bottom = self.portrait_slot.bottom
        print("active spell slot is: ", self.active_spell_slot)

    def draw(self, disp):
        # self.image.blit(self.portrait, self.portrait_slot)
        # self.image.blit(self.book_image, self.book_slot)
        # for x in range(0, len(self.spell_list)):
        #     self.image.blit(self.spell_list[x].image, self.active_spell_slot.move(x*self.spell_list[x].rect.width,
        #                                                                           0))
        #                                                                           #self.spell_list[x].rect.height))
        # #self.image.blit(self)
        # disp.blit(self.image, self.rect)
        disp.blit(self.portrait, self.portrait_slot)
        disp.blit(self.book_image, self.book_slot)
        for x in range(0, len(self.spell_list)):
            disp.blit(self.spell_list[x].image, self.active_spell_slot.move(x * self.spell_list[x].rect.width,
                                                                            0))
                                                                            #self.spell_list[x].rect.height))