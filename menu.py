import pygame, spriteling, config

menu_default = pygame.image.load('overlays\img_menu_default.png').convert()

width = config.screen_size[0]
height = config.screen_size[1]
p1_rect = pygame.rect.Rect((      0,        0), (width/2, height/2))
p2_rect = pygame.rect.Rect((width/2,        0), (width/2, height/2))
p3_rect = pygame.rect.Rect((      0, height/2), (width/2, height/2))
p4_rect = pygame.rect.Rect((width/2, height/2), (width/2, height/2))

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
        self.ready = False
        self.book_img = unlocked_books[self.index]
        self.player_img = unlocked_books[self.index].

    def next_book(self):
        self.index += 1

    def prev_book(self):
        self.index -= 1

    def update(self, **kwargs):
        if 'locked' in kwargs:
            while(self.index in kwargs['locked']):
                self.index += 1
                if self.index >= len(self.book_choice):
                    self.index = 0



class button(spriteling.spriteling):
    def __init__(self):
        super().__init__()
