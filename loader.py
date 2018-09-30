import pygame

class image_loader():
    pass

light_wave_img = pygame.image.load(      'projectiles\img_blast.png').convert_alpha()
fire_ball_img  = pygame.image.load(   'projectiles\img_fireball.png').convert_alpha()
acid_ball_img  = pygame.image.load( 'projectiles\img_poisonball.png').convert_alpha()
icy_ball_img   = pygame.image.load(    'projectiles\img_iceball.png').convert_alpha()

basic_books    = pygame.image.load('projectiles\img_basic_books.png').convert_alpha()
ice_book_img   = basic_books.subsurface(( 0,  0), (20, 20))
fire_book_img  = basic_books.subsurface(( 0, 20), (20, 20))
acid_book_img  = basic_books.subsurface(( 0, 40), (20, 20))
light_book_img = basic_books.subsurface(( 0, 60), (20, 20))
blank_book_img = basic_books.subsurface(( 0, 60), (20, 20))


bigger_books = pygame.transform.scale2x(basic_books)

class player_img_loader():
    def __init__(self):
        goddess_robes     =  pygame.image.load('people\img_goddess1.png').convert_alpha()
        goddess_crop_top  =  pygame.image.load('people\img_goddess2.png').convert_alpha()
        goddess_body_suit =  pygame.image.load('people\img_goddess3.png').convert_alpha()
        goddess_tattered  =  pygame.image.load('people\img_goddess4.png').convert_alpha()
        self.img_lookup ={'robes': goddess_robes,
                          'crop_top': goddess_crop_top,
                          'body_suit': goddess_body_suit,
                          'tattered': goddess_tattered,
                         }

    def get_sheet(self, lookup, size_mult=0):
        scale = size_mult
        ret = self.img_lookup[lookup]
        while scale > 0:
            # ret = pygame.rect.Rect((0, 0), ())
            pygame.transform.scale2x(self.img_lookup[lookup], ret)
        return ret

    def __call__(self, lookup, index, size_mult=0):
        ref = self.get_sheet(lookup, size_mult)
        size = ref.get_rect()
        h = size.height/3
        w = size.width/4
        return ref.subsurface((w*index[0],  h*index[1]), (w, h))
