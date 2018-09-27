

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

    def attach_player(self, user):
        self.player = user

    def attach_book(self, spellbook):
        self.book = spellbook

    def draw_contents(self, disp):
        self.player.draw(disp)
        self.book.draw(disp)