import pygame

# all-purpose handler class that coordinates the player, controller, and whatever else needs coordinating
# this is what allows a seamless transition between menu/game loops, keeps everything modular and independent, and
# solves a ton of headache causing problems with scope resolution
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
        self.missiles = pygame.sprite.Group()

    def attach(self, **kwargs):
        if 'player' in kwargs:
            self.player = kwargs['player']
        if 'book' in kwargs:
            self.book = kwargs['book']
        if 'menu' in kwargs:
            self.menu = kwargs['menu']

    def update_menu(self):
        #print("performing a menu update from player handler")
        #print("controller is type: ", type(self.controller))
        self.controller.update()
        face = self.controller.pull_face()
        A_accept = face['accept']
        Start_accept = face['start']
        selection = self.controller.pull_selectors()
        next = selection['next']
        prev = selection['prev']
        #print("selection is: ", selection)
        if next[1] and not next[0]:
            self.menu.next_book()
        elif prev[1] and not prev[0]:
            self.menu.prev_book()
        if (A_accept[1] and not A_accept[0]) or (Start_accept[1] and not Start_accept[0]):
            self.attach(book=self.menu.ready_up())

    def update(self, *args, **kwargs):
        # print("interface update: ", self)
        # updates the controller
        self.controller.update()

        #updates the player
        movement = self.controller.pull_movement()['move']
        facing = self.controller.pull_movement()['look']
        #self.player.move(move=movement)
        self.player.update(look=facing, move=movement)

        # updates the spellbook
        now, prev = self.controller.pull_face()['fire']
        # print("now= ", now, "prev= ", prev)
        sel_chk = self.controller.pull_selectors()['select']
        nxt_chk = self.controller.pull_selectors()['next']
        prv_chk = self.controller.pull_selectors()['prev']
        # its safe to call update more than once per frame for the spell book
        origin = self.player.rect.center
        if sel_chk != 9:
            self.book.update(origin, select_spell=sel_chk)
        elif nxt_chk[0] and not nxt_chk[1]:
            self.book.update(origin, cycle_spell='next')
        elif prv_chk[0] and not prv_chk[1]:
            self.book.update(origin, cycle_spell='prev')
        if now or prev:
            self.book.update(origin, fire=(now, prev), direction=self.player.facing,
                             missile_layer=self.missiles)

        # updates spells
        self.missiles.update()

    def begin_game(self, p_constr, starting_room):
        self.player = p_constr(self.book)
        self.book.pop_spells()
        import overlays
        self.hud = overlays.hud(self.player, self.book)
        starting_room.add_players(self.player)

    def draw(self, disp):
        self.player.draw(disp)
        self.player.draw_boxes(disp)
        self.missiles.draw(disp)
        for each in self.missiles:
            each.draw_boxes(disp)
        self.book.active_spell.draw(disp)
        self.hud.draw(disp)
        self.hud.draw_boxes(disp)
