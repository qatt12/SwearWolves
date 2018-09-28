import pygame, spriteling

menu_default = pygame.image.load('overlays\img_menu_default.png').convert()

class menu(spriteling.spriteling):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = menu_default


class player_select_menu(menu):
    def __init__(self, rect, unlocked_books):
        super().__init__(rect)
        self.possible_books = unlocked_books
        self.index = 0


class button(spriteling.spriteling):
    def __init__(self):
        super().__init__()
