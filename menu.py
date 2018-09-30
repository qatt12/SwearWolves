import pygame, spriteling, config

menu_default = pygame.image.load('overlays\img_menu_default.png').convert()

half_screen_width = config.screen_size[0]/2
half_screen_height = config.screen_size[1]/2
p1_rect = pygame.rect.Rect((0, 0), (half_screen_width, half_screen_height))
p2_rect = pygame.rect.Rect((half_screen_width, 0), (half_screen_width, half_screen_height))
p3_rect = pygame.rect.Rect((0, half_screen_height), (half_screen_width, half_screen_height))
p4_rect = pygame.rect.Rect((half_screen_width, half_screen_height), (half_screen_width, half_screen_height))
p_lookup = {1: p1_rect, 2: p2_rect, 3: p3_rect, 4: p4_rect}

class menu(spriteling.spriteling):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = menu_default


class player_select_menu(menu):
    def __init__(self, player_num, unlocked_books):
        super().__init__(p_lookup[player_num])
        self.index = 0
        self.book_choice = unlocked_books

    def next_book(self):
        pass

    def update(self, **kwargs):
        if 'locked' in kwargs:
            pass


class button(spriteling.spriteling):
    def __init__(self):
        super().__init__()
