
# all-purpose handler class that coordinates the player, controller, and whatever else needs coordinating
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

    def attach(self, **kwargs):
        if 'player' in kwargs:
            self.player = kwargs['player']
        if 'book' in kwargs:
            self.player = kwargs['book']
        if 'menu' in kwargs:
            self.menu = kwargs['menu']

    def update_menu(self):
        self.controller.update()
        face = self.controller.pull_face()
        A_accept = face['accept']
        Start_accept = face['start']
        selection = self.controller.pull_selectors()
        next = selection['next']
        prev = selection['prev']
        if next[1] and not next[0]:
            self.menu.next_book()
        elif prev[1] and not prev[0]:
            self.menu.prev_book()
        if (A_accept[1] and not A_accept[0]) or (Start_accept[1] and not Start_accept[0]):
            self.attach(book=self.menu.ready_up())

    def update(self, *args, **kwargs):
        self.controller.update()

