import pygame, spriteling, config

menu_default = pygame.image.load('overlays\img_menu_default.png').convert()

width = config.screen_size[0]
height = config.screen_size[1]
print("in menu.py, config width, height is: ", width, ", ", height)
print("in menu.py, half width, height is: ",width/2, ", ", height/2)
p1_rect = pygame.rect.Rect((      0,        0), (width/2, height/2))
p2_rect = pygame.rect.Rect((width/2,        0), (width/2, height/2))
p3_rect = pygame.rect.Rect((      0, height/2), (width/2, height/2))
p4_rect = pygame.rect.Rect((width/2, height/2), (width/2, height/2))

p_lookup = {1: p1_rect, 2: p2_rect, 3: p3_rect, 4: p4_rect}

p_rect =  pygame.rect.Rect((      0,        0), (width/2, height/2))

from config import color_lookup as c_lookup

from loader import player_img_loader
ld_plyr = player_img_loader()

class menu(spriteling.spriteling):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = menu_default

    def draw(self, *args):
        pass


class player_select_menu(menu):
    def __init__(self, player_num, unlocked_books):
        super().__init__(p_lookup[player_num])
        w, h = int(width/2), int(height/2)
        #print("in menu.py, half width, height is: ", w, ", ", h)
        self.id_no = player_num
        self.image = pygame.Surface((w, h))
        self.color = c_lookup[player_num]
        self.index = 0
        self.book_choice = unlocked_books
        self.ready = False
        self.curr_book_img = pygame.transform.scale2x(unlocked_books[self.index].image)
        self.player_img = pygame.transform.scale2x(ld_plyr(unlocked_books[self.index].goddess_lookup_key, (1, 1)))

    def next_book(self):
        if not self.ready:
            self.index += 1
            if self.index >= len(self.book_choice):
                self.index = 0
            self.curr_book_img = pygame.transform.scale2x(self.book_choice[self.index].image)
            self.player_img = pygame.transform.scale2x(ld_plyr(self.book_choice[self.index].goddess_lookup_key, (1, 1)))

    def prev_book(self):
        if not self.ready:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.book_choice)-1
            self.curr_book_img = pygame.transform.scale2x(self.book_choice[self.index].image)
            self.player_img = pygame.transform.scale2x(ld_plyr(self.book_choice[self.index].goddess_lookup_key, (1, 1)))

    def ready_up(self):
        self.ready = True
        return self.book_choice[self.index]

    def is_ready(self):
        if self.ready:
            return self.index
        else:
            return -1

    def back_out(self):
        if not self.ready:
            self.kill()
        else:
            self.ready = False

    # ignore this for now; doesn't really work
    def ban_book(self, index_no):
        new_list = []
        for x in range(0, len(self.book_choice)):
            if x != index_no:
                new_list.append(self.book_choice[x])
        self.book_choice = new_list
        if self.index > len(self.book_choice):
            self.index = len(self.book_choice)

    def update(self, **kwargs):
        if not self.ready:
            from config import black
            self.image.fill(black)
            self.curr_book_img = pygame.transform.scale2x(self.book_choice[self.index].image)
            self.player_img = pygame.transform.scale2x(ld_plyr(self.book_choice[self.index].goddess_lookup_key, (1, 1)))

        elif self.ready:
            pygame.draw.rect(self.image, self.color, p_rect, 40)

        self.image.blit(self.curr_book_img, (((p_rect.width / 2) - self.curr_book_img.get_rect().width / 2),
                                               (p_rect.height) - self.curr_book_img.get_rect().height))

        self.image.blit(self.player_img, (((p_rect.width / 2) - self.player_img.get_rect().width / 2),
                                    (p_rect.height / 2) - self.player_img.get_rect().height / 2))
        pygame.draw.rect(self.image, self.color, p_rect, 4)

    def draw(self, disp):
       # print("calling player select menu draw")
        disp.blit(self.image, self.rect)


class button(spriteling.spriteling):
    def __init__(self, subj):
        super().__init__(image=subj.image)


class button_wheel(menu):
    def __init__(self, rect, *args):
        super().__init__(rect)
        self.content = [button(each) for each in args]
