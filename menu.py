import pygame, spriteling

class menu(spriteling.spriteling):
    def __init__(self):
        super().__init__()

class player_select_menu(menu):
    def __init__(self, unlocked_books):
        super().__init__()
        self.possible_books = unlocked_books
        self.index = 0
