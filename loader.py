import pygame

class image_loader():
    pass

# light_wave_img = pygame.image.load(      'projectiles\img_blast.png').convert_alpha()
# fire_ball_img  = pygame.image.load(   'projectiles\img_fireball.png').convert_alpha()
# acid_ball_img  = pygame.image.load( 'projectiles\img_poisonball.png').convert_alpha()
# icy_ball_img   = pygame.image.load(    'projectiles\img_iceball.png').convert_alpha()
#
# basic_books    = pygame.image.load('projectiles\img_basic_books.png').convert_alpha()
# ice_book_img   = basic_books.subsurface(( 0,  0), (20, 20))
# fire_book_img  = basic_books.subsurface(( 0, 20), (20, 20))
# acid_book_img  = basic_books.subsurface(( 0, 40), (20, 20))
# light_book_img = basic_books.subsurface(( 0, 60), (20, 20))
# blank_book_img = basic_books.subsurface(( 0, 60), (20, 20))


#bigger_books = pygame.transform.scale2x(basic_books)

class player_img_loader():
    def __init__(self):
        goddess_robes     =  pygame.image.load('Animation\img_goddess1.png').convert()
        goddess_crop_top  =  pygame.image.load('Animation\img_goddess2.png').convert()
        goddess_body_suit =  pygame.image.load('Animation\img_goddess3.png').convert()
        goddess_tattered  =  pygame.image.load('Animation\img_goddess4.png').convert()
        goddess_robes.set_colorkey((255, 174, 201))
        goddess_crop_top.set_colorkey((255, 174, 201))
        goddess_body_suit.set_colorkey((255, 174, 201))
        goddess_tattered.set_colorkey((255, 174, 201))
        self.img_lookup ={'robes': goddess_robes,
                          'crop_top': goddess_crop_top,
                          'body_suit': goddess_body_suit,
                          'tattered': goddess_tattered,
                         }

    def get_sheet(self, lookup):
        return self.img_lookup[lookup]

    def __call__(self, lookup, index, size_mult=0):
        ref = self.get_sheet(lookup)
        size = ref.get_rect()
        h = size.height/3
        w = size.width/4
        return ref.subsurface((w*index[0],  h*index[1]), (w, h))


class save_file():
    pass