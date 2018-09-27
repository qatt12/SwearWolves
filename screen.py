import pygame

class menu_screen(pygame.sprite.Group):
    def __init__(self, size, **kwargs):
        super().__init__()
        self.size = size
        if 'mode' in kwargs:
            self.mode = kwargs['mode']
        else:
            self.mode = 'start'
