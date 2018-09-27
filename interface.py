import pygame, player, spells, controllers

class interface():
    def __init__(self, controller, **kwargs):
        self.controller = controller
        if 'player' in kwargs:
            self.player = kwargs['player']
        else:
            self.player = None
        if 'book' in kwargs:
            self.player = kwargs['book']
        else:
            self.book = None

