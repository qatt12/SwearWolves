import pygame, events, config
from events import event_maker


class box():
    def __init__(self, *args, **kwargs):
        self.values = [each for each in args]
        for each in kwargs:
            pass

class facing_angle():
    def __init__(self, x_dir, y_dir):
        y_pos_set = {'up', 'top', '+1', '1', 1}
        y_neg_set = {'down', 'bottom', 'btm', '-1', -1}

        if y_dir in y_pos_set:
            self.y_dir = 1
        elif y_dir in y_neg_set:
            self.y_dir = -1
        else:
            self.y_dir = 0

        x_pos_set = {'right', 'rht', '1', '+1', 1}
        x_neg_set = {'left', 'lft', '-1', -1}

        if x_dir in x_pos_set:
            self.x_dir = 1
        elif x_dir in x_neg_set:
            self.x_dir = -1
        else:
            self.x_dir = 0

    def __str__(self):
        if self.x_dir == 0:
            x_ret = ""
        elif self.x_dir > 0:
            x_ret = "right"
        elif self.x_dir < 0:
            x_ret = "left"
        if self.y_dir == 0:
            y_ret = ""
        elif self.y_dir > 0:
            y_ret = "up"
        elif self.y_dir < 0:
            y_ret = "down"
        return x_ret + y_ret

    def __call__(self, new_dir_x, new_dir_y, locked=False):
        lock_y, lock_x = False, False
        if locked:
            base = (self.x_dir, self.y_dir)
            if self.x_dir == 0 and self.y_dir != 0:
                if new_dir_x > 0:
                    self.x_dir = 1
                elif new_dir_x < 0:
                    self.x_dir = -1
            elif self.y_dir == 0 and self.x_dir != 0:
                if new_dir_y > 0:
                    self.y_dir = 1
                elif new_dir_y < 0:
                    self.y_dir = -1
                else:
                    self.y_dir = 0
            elif self.x_dir == 0 and self.x_dir == 0:
                return (0, 0)
            else:
                if self.x_dir < 0 < new_dir_x or self.x_dir > 0 > new_dir_x:
                        self.x_dir = 0
                if self.y_dir < 0 < new_dir_y or self.y_dir > 0 > new_dir_y:
                    self.y_dir = 0
        else:
            if new_dir_x > 0:
                self.x_dir = 1
            elif new_dir_x < 0:
                self.x_dir = -1
            else:
                self.x_dir = 0
            if new_dir_y > 0:
                self.y_dir = 1
            elif new_dir_y < 0:
                self.y_dir = -1
            else:
                self.y_dir = 0
        return (self.x_dir, self.y_dir)



    @classmethod
    def from_bool(cls, by_bool_a, by_bool_b):
        pass

    @classmethod
    def from_int(cls, int_a, int_b):
        pass

    @classmethod
    def from_string(cls, descr):
        y_pos_set = {'up', 'top'}
        y_neg_set = {'down', 'bottom'}




# all-purpose handler class that coordinates the player, controller, and whatever else needs coordinating
# this is what allows a seamless transition between menu/game loops, keeps everything modular and independent, and
# solves a ton of headache causing problems with scope resolution
class handler():
    num_player_interfaces = 0

    @classmethod
    def add_player_interface(cls):
        cls.num_player_interfaces +=1

    @classmethod
    def get_player_interface_num(cls):
        return cls.num_player_interfaces

    @classmethod
    def next_player_interface(cls):
        cls.add_player_interface()
        return cls.get_player_interface_num()

    def __init__(self, controller, **kwargs):
        self.number = handler.next_player_interface()
        # the bare minimum a handler needs is a controller (coincidentally, this is the bare minimum case in which a
        # handler is useful). It only takes a controller at first because the first handler is made right after the
        # driver.py::start loop is set to end (when player one hits start). At that point, a controller is all thats
        # available to be passed into class::handler
        self.controller = controller

        # most of this kwargs stuff is nearly useless, artifacts of a different version or stuff I added in case I
        # wanted to change it later, or I thought it would be easy to expand functionality in this direction
        # for whatever values aren't specified in kwargs, the initial state(s) are set to None, because handler needs
        # that field, but it can't be filled yet. They are added to handler via the attach method
        message = events.entry('log', 'new player', 'a new player_handler has been initialized', 'interface', True, True,
                               'player', 'once', 'player_handler', 'handler',
                               inst_src=self, obj_src='interface.handler', controller=self.controller, found_kwargs=kwargs,
                               num_of_player_handlers=handler.get_player_interface_num())
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'generic'
        message.modify(name=self.name)
        if 'player' in kwargs:
            self.player = kwargs['player']
            message.modify(player=self.player)
        else:
            self.player = None
        if 'book' in kwargs:
            self.player = kwargs['book']
            message.modify(book=self.book)
        else:
            self.book = None
        if 'menu' in kwargs:
            self.menu = kwargs['menu']
            message.modify(menu=self.menu)
        else:
            self.menu = None
        self.hud = None
        self.my_reticle = None
        self.missiles = pygame.sprite.Group()
        self.my_player_single = pygame.sprite.GroupSingle()
        self.other_players = pygame.sprite.Group()
        self.known_enemies = pygame.sprite.Group()
        self.my_marker = None

        self.layer = config.player_layer
        self.new_spell = True
        self.spell_layer = config.player_layer + self.number

    # method used to attach various important member vars to a player object that already exists
    def attach(self, **kwargs):
        message = events.entry('trace', 'player handler attachments', 'the things that have been successfully attached to this player handler', 'interface',
                               'player', 'book', 'player_name',
                               inst_src=self)
        if 'player' in kwargs:
            self.player = kwargs['player']
            message.modify(player=self.player)
        if 'book' in kwargs:
            self.book = kwargs['book']
            message.modify(book=self.book)
        if 'menu' in kwargs:
            self.menu = kwargs['menu']
            message.modify(menu=self.menu)
        if 'name' in kwargs:
            self.name = kwargs['name']
            message.modify(my_name=self.name)
        if 'impact' in kwargs:
            self.missiles.add(kwargs['impact'])
            #if self.my_marker == None:
            #    self.my_marker =
            #elif self.my_marker.rect.center != kwargs['impact']:
            #    self.missiles.add()
            message.modify(new_impact=kwargs['impact'])
        event_maker.send_entry(message)

    def update_menu(self):
        event_maker.make_entry('trace', 'menu_update', '', 'interface', False, False,
                               'player', 'menu', 'update', 'quagmire',
                               obj_src=handler, inst_src=self)
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

    def update(self, **kwargs):
        # updates the controller
        self.controller.update()
        # updates the player
        facing = self.controller.pull_movement()['look']
        movement = self.controller.pull_movement()['move']
        stick_data = self.controller.pull_movement()
        interaction = self.controller.pull_face()['interact']
        lock_next = self.controller.pull_face()['lock_next']
        lock_next = lock_next[0] and not lock_next[1]
        lock_prev = self.controller.pull_face()['lock_prev']
        lock_prev = lock_prev[0] and not lock_prev[1]
        self.player.update(look=facing, move=movement, interact=interaction, stick_data=stick_data)
        special = self.controller.pull_face()['back']

        # updates the spellbook
        now, prev = self.controller.pull_face()['fire']
        # print("now= ", now, "prev= ", prev)
        sel_chk = self.controller.pull_selectors()['select']
        nxt_chk = self.controller.pull_selectors()['next']
        prv_chk = self.controller.pull_selectors()['prev']
        # its safe to call update more than once per frame for the spell book
        origin = self.player.rect.center
        if sel_chk != 9:
            self.new_spell = self.book.select_spell(select_spell=sel_chk)
        elif nxt_chk[0] and not nxt_chk[1]:
            self.new_spell = self.book.select_spell(cycle_spell='next')
        elif prv_chk[0] and not prv_chk[1]:
            self.new_spell = self.book.select_spell(cycle_spell='prev')
        else:
            self.new_spell = False
        self.book.update(origin, fire=(now, prev), direction=self.player.facing,
                         missile_layer=self.missiles, targ_lock=(lock_next-lock_prev), reticle=self.my_reticle,
                         special=special, **kwargs)

        # updates spells
        # I just need to get the targeting data into the targeted spell
        self.missiles.update()

        dump_trigger = self.controller.pull_face()['select']
        if dump_trigger[0] != dump_trigger[1]:
            event_maker.flush_trace_buffer()
            event_maker.new_event(events.game_state_event, 'interface', subtype='end_game')

    # finishes pre-game prep by populating all of the necessary internal vars with the applicable data/references.
    # called by driver.py::class::screen. p_constr had to be passed in as a param to avoid importing stuff to
    # interface.py (which totally makes sense for reasons that are great and super important)
    def begin_game(self, p_constr, starting_room, player_num, music=False):
        # deletes a reference to the char_select_menu, since it is no longer needed, and should be garbage collected
        self.menu = None
        self.player = p_constr(self.book, self.number)
        from overlays import select_reticle
        self.book.set_my_player_HANDLER(self)
        self.book.pop_spells(select_reticle(self.number))
        # okay so I couldn't get around importing this one thing.
        from overlays import hud
        self.hud = hud(self.player, self.book, player_num)
        starting_room.add_player(self.player)
        self.my_player_single.add(self.player)
        if music:
            pygame.mixer.music.load('Music/LoLD.ogg')
            pygame.mixer.music.play(-1)

    # all of the draw_boxes method calls are for debugging and uses should be deleted prior to submission
    def draw(self, disp, boxes=False):
        self.player.draw(disp)
        self.book.draw(disp)
        self.missiles.draw(disp)
        if boxes:
            self.player.draw_boxes(disp)

################## how to properly get spells into driver

    def get_hud(self):
        return self.hud

    def get_spells(self):
        return {'refresh': self.new_spell,
            'active': self.book.get_active_spell()[1],
        "inactive": self.book.other_spells}

    def get_missiles(self):
        return self.missiles

    def add(self, *args, **kwargs):
        self.attach(**kwargs)

    def apply_to_player(self, effects):
        pass
