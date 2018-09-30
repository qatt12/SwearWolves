

class handler():
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
        if 'menu' in kwargs:
            self.menu = kwargs['menu']
        else:
            self.menu = None
        self.hud = None

    def update(self, *args):
        pass