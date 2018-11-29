import pygame, spriteling, config
from config import hud_width_proportion as width_scalar
from config import hud_height_proportion as height_scalar

hp_bar_width = 20

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

    def draw(self, disp, boxes=False):
        #print("drawing a hud")
        disp.blit(self.portrait, self.portrait_slot)
        disp.blit(self.book_image, self.book_slot)
        for x in range(0, len(self.spell_list)):
            disp.blit(self.spell_list[x].image, self.active_spell_slot.move(x * self.spell_list[x].rect.width,
                                                                            0))
                                                                            #self.spell_list[x].rect.height))
        pygame.draw.line(disp, config.green, (self.portrait_slot.right, self.portrait_slot.centery),
                         (self.portrait_slot.right+(self.hp/2), self.portrait_slot.centery), hp_bar_width)


all_reticles = pygame.image.load('Animation\img_crosshair.png').convert_alpha()
green_reticle = pygame.transform.scale2x(all_reticles.subsurface((0, 0), (54, 54)))
red_reticle = pygame.transform.scale2x(all_reticles.subsurface((54, 0), (54, 54)))
blue_reticle = pygame.transform.scale2x(all_reticles.subsurface((54 * 2, 0), (54, 54)))
reticle_lookup = {
    0: green_reticle,
    1: red_reticle,
    2: blue_reticle,
    3: green_reticle
}


class reticle(spriteling.spriteling):
    def __init__(self, designation):
        super().__init__(image=reticle_lookup[designation])
        self.layer = config.spark_layer

    def update(self, *args, **kwargs):
        if 'new_target' in kwargs:
            self.rect.center = kwargs['new_target'].rect.center
        if 'position' in kwargs:
            self.rect.center = kwargs["position"]

    def __call__(self, *args, **kwargs):
        pass

class p1_reticle(reticle):
    def __init__(self):
        super().__init__(0)

class p2_reticle(reticle):
    def __init__(self):
        super().__init__(1)

class p3_reticle(reticle):
    def __init__(self):
        super().__init__(2)

def select_reticle(num):
    lookup = {
        0: p1_reticle,
        1: p2_reticle,
        2: p3_reticle
    }
    return lookup[num]