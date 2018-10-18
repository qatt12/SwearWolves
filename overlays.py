import pygame, spriteling

class hud(spriteling.spriteling):
    def __init__(self, player, book, *args, **kwargs):
        super().__init__()
        self.book_image = book.image
        self.portrait = player.image
        self.spell_list = [book.spells]
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
