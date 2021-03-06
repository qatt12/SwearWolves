# rooms are a sort of container class that hold and manage their contents.
# as self-evident as the above sounds, it is an important note

import pygame, blocks, config, random, events, collections, spriteling
from events import event_maker
sGroup = pygame.sprite.Group

from blocks import wall as wall
from blocks import corner as corner
from blocks import floor as floor
from blocks import door as door
from config import tile_scalar
from spriteling import hitbox
from spriteling import collide_hitbox

# essentially an image lookup/helper tool for room. contains all the default tiles for the default room, but can be
# subclassed to create new themes
class theme(object):
    def __init__(self):
        # the default is just a placeholder, and references assets from the proto game
        floor = pygame.image.load('Animation\img_tile.png').convert_alpha()
        tlcrnr = pygame.image.load("Animation\img_corner_tl.png").convert_alpha()
        trcrnr = pygame.image.load("Animation\img_corner_tr.png").convert_alpha()
        blcrnr = pygame.image.load("Animation\img_corner_bl.png").convert_alpha()
        brcrnr = pygame.image.load("Animation\img_corner_br.png").convert_alpha()
        topWall = pygame.image.load("Animation\img_wall.png").convert_alpha()
        btmWall = pygame.image.load('Animation\img_wall_d.png').convert_alpha()
        rgtWall = pygame.image.load('Animation\img_wall_r.png').convert_alpha()
        lftWall = pygame.image.load('Animation\img_wall_l.png').convert_alpha()
        # tile set lookup
        self.image_lookup = {'f': floor,
                             'trc': trcrnr, 'tlc': tlcrnr, 'blc': blcrnr, 'brc': brcrnr,
                             'tw': topWall, 'bw': btmWall, 'rw': rgtWall, 'lw': lftWall}

    # creates a simple rectangular outer wall, and returns a group with all the new wall spritelings
    # NOTE: probably should modify this to make use of the attach method so walls can be conveniently scrolled around
    def build_walls(self, border, enter_from, entry_door):
        all_walls = sGroup()
        # spawns and positions the outer wall pieces. Note the i + 50 and j + 50: this cause the wall segments to
        # slightly overlap w/ the corner segments' rects, thus properly enclosing the room
        for i in range(border.left - int(tile_scalar/2), border.right + int(tile_scalar/2), tile_scalar):
            top = wall('up', self.image_lookup['tw'], (i + 50, border.top))
            # print("top wall: \n Rect: ",top.rect, "hitbox: ", top.hitbox.rect)

            bottom = wall('down', self.image_lookup['bw'], (i + 50, border.bottom))
            # print("bottom wall: \n Rect: ", bottom.rect, "hitbox: ", bottom.hitbox.rect)

            if enter_from[0] == 'top' and enter_from[1] == (i/tile_scalar):
                entry_door.attach(top, (0, 0))
            elif enter_from[0] == 'top' and enter_from[1] == (i/tile_scalar):
                entry_door.attach(bottom, (0, 0))
            all_walls.add(top, bottom)
        for j in range(border.top - int(tile_scalar/2), border.bottom + int(tile_scalar/2), tile_scalar):
            left = wall('left', self.image_lookup['lw'], (border.left, j + 50))
            right = wall('right', self.image_lookup['rw'], (border.right, j + 50))
            if enter_from[0] == 'left' and enter_from[1] == (j / tile_scalar):
                entry_door.attach(left, (0, 0))
            elif enter_from[0] == 'right' and enter_from[1] == (j / tile_scalar):
                entry_door.attach(right, (0, 0))
            all_walls.add(left, right)

        all_walls.add(corner('top_left', self.image_lookup['tlc'], border.topleft))
        all_walls.add(corner('bottom_left', self.image_lookup['blc'], border.bottomleft))
        all_walls.add(corner('top_right', self.image_lookup['trc'], border.topright))
        all_walls.add(corner('bottom_right', self.image_lookup['brc'], border.bottomright))

        return all_walls

    def build_inner_walls(self, **kwargs):
        all_walls  = pygame.sprite.Group()
        if 'rect' in kwargs:
            border = kwargs['rect']
            for i in range(border.left - int(tile_scalar/2), border.right + int(tile_scalar/2), tile_scalar):
                top = wall('up', self.image_lookup['tw'], (i + 50, border.top))
                bottom = wall('down', self.image_lookup['bw'], (i + 50, border.bottom))
                all_walls.add(top, bottom)
            for j in range(border.top - int(tile_scalar/2), border.bottom + int(tile_scalar/2), tile_scalar):
                left = wall('left', self.image_lookup['lw'], (border.left, j + 50))
                right = wall('right', self.image_lookup['rw'], (border.right, j + 50))
                all_walls.add(left, right)

            all_walls.add(corner('top_left', self.image_lookup['tlc'], border.topleft))
            all_walls.add(corner('bottom_left', self.image_lookup['blc'], border.bottomleft))
            all_walls.add(corner('top_right', self.image_lookup['trc'], border.topright))
            all_walls.add(corner('bottom_right', self.image_lookup['brc'], border.bottomright))

            return all_walls

default_theme = theme()

event_maker.make_entry('log', 'default_theme', 'Testing default theme construction/initialization', 'room', True, False, 'theme', 'init', 'DEBUG', obj_src=default_theme, image_lookup=default_theme.image_lookup)

enemies_layer = 6
wall_cos = 5
doors_layer = 4
inner_walls_layer = 3
outer_walls_layer = 2
floor_cos = 1
floor_layer = 0
# the core functions of the room are to hold everything that is going to appear on the screen, check for and report the
# interactions between certain sprites, and to draw everything in the correct order
class room():
    def __init__(self, enter_from, size, disp, my_theme, *args, **kwargs):


        event_maker.make_entry('trace', 'room init', 'Room constructor has been invoked', 'room', False, False,
                               'room', 'init', 'waffles',
                               found_kwargs=kwargs)
        # the constructor reqs a size tuple for height and width in tiles, a theme from which to draw tiles and enemies,
        # the current difficulty level, and the player's point of entry.
        self.image = pygame.Surface(size)
        self.contents = pygame.sprite.LayeredUpdates()
        self.ordered_enemies = collections.deque([])

        # the floor(s) are interesting. in order to allow the creation of irregularly shaped (non-rectangular) floors,
        # each segment of floor is created separately, then linked together. upon first being initialized, a room has a
        # simple, rectangular floor enclosed in a bounding wall.
        self.ground = floor(size, my_theme)
        self.contents.add(self.ground, layer=floor_layer)

        # this is supposed to help with screen scrolling for the room. The visible rect is what is currently on-screen,
        # the full rect is for the entire room
        self.visible_rect = disp.get_rect()
        self.full_rect = self.ground.rect
        #self.full_rect.inflate_ip(100, 100)
        self.scroll_rect = self.visible_rect.inflate(-150, -150)
        self.scroll_rect.center = self.visible_rect.center
        self.hazards = pygame.sprite.Group()

        self.entry_door = self.add_entrance(enter_from[0], enter_from[1])
        self.contents.add(self.entry_door, layer=doors_layer)
        if "exit_door" in kwargs:
            event_maker.make_entry('trace', 'exit_door', 'found kwarg entry for exit door', 'room', True, False,
                                   'door', 'exit', 'kwargs',
                                   obj_src=room, inst_src=self, exit_doors=kwargs['exit_door'])
            for each in kwargs['exit_door']:
                self.contents.add(self.add_door(each[0], each[1]), layer=doors_layer)
        else:
            print("making an exit")
            num_doors = random.randint(1, 3)
            which_wall = {1: 'top', 2: 'bottom', 3: 'right'}
            for x in range(0, num_doors):
                self.contents.add(self.add_door(which_wall[random.randint(1, 3)], random.randint(2, size[1])), layer=doors_layer)

        # the walls have to be spritelings in a group in order to properly register collision
        self.contents.add(my_theme.build_walls(self.full_rect, enter_from, self.entry_door), layer=outer_walls_layer)

        self.nodes = [spriteling.nodebox(x, y, config.tile_scalar, config.tile_scalar)
                      for x in range(self.full_rect.left, self.full_rect.right, config.tile_scalar)
                      for y in range(self.full_rect.top, self.full_rect.bottom, config.tile_scalar)]

        if 'inner_wall_rect' in kwargs:
            inner_wall_temp = kwargs['inner_wall_rect'].clamp(self.full_rect)
            self.nodes = [each for each in self.nodes
                          if not each.rect.colliderect(inner_wall_temp)]
            self.contents.add(my_theme.build_inner_walls(rect=inner_wall_temp), layer=inner_walls_layer)
        elif 'inner_wall_rects' in kwargs:
            for each in kwargs['inner_wall_rects']:
                inner_wall_temp = each.clamp(self.full_rect)
                self.nodes = [each for each in self.nodes
                              if not each.rect.colliderect(inner_wall_temp)]
                self.contents.add(my_theme.build_inner_walls(rect=inner_wall_temp), layer=inner_walls_layer)
        event_maker.make_entry('trace', 'door init', "", 'room', False, False,
                               'door', 'init',
                               door_rect_at_init=self.entry_door.rect)

        self.all_walls = pygame.sprite.Group(self.contents.get_sprites_from_layer(outer_walls_layer),
                                             self.contents.get_sprites_from_layer(inner_walls_layer))
        if "pit_rect" in kwargs:
            pit_rect_temp = kwargs['pit_rect'].clamp(self.ground.rect)
            self.nodes = [each for each in self.nodes
                          if not each.rect.colliderect(pit_rect_temp)]
            print("floor: ", self.ground.rect)
            print("pit: ", pit_rect_temp)
            if 'bridge_rect' in kwargs:
                bridge_temp = kwargs['bridge_rect'].clamp(self.ground.rect)
                print("pit_rect_temp.height-(bridge_temp.top = ", pit_rect_temp.height-(bridge_temp.top))
                pit_rect_a = pygame.rect.Rect((pit_rect_temp.left, pit_rect_temp.top), (pit_rect_temp.width, int(pit_rect_temp.height-(bridge_temp.top)))).clamp(self.full_rect)
                pit_rect_b = pygame.rect.Rect(( pit_rect_temp.left, bridge_temp.bottom), (pit_rect_temp.width, int(bridge_temp.top-bridge_temp.bottom))).clamp(self.full_rect)
                pit_a = blocks.pit(pit_rect_a)
                self.hazards.add(pit_a)
                self.contents.add(pit_a, layer=pit_a.layer)
                pit_b = blocks.pit(pit_rect_b)
                self.hazards.add(pit_b)
                self.contents.add(pit_b, layer=pit_b.layer)
            else:
                pit = blocks.pit(pit_rect_temp)
                self.hazards.add(pit)
                self.contents.add(pit, layer=pit.layer)
        if "pit_rects" in kwargs:
            for each in kwargs['pit_rects']:
                pit_rect_temp = each.clamp(self.ground.rect)
                self.nodes = [each for each in self.nodes
                              if not each.rect.colliderect(pit_rect_temp)]
                print("floor: ", self.ground.rect)
                print("pit: ", pit_rect_temp)
                pit = blocks.pit(pit_rect_temp)
                self.hazards.add(pit)
                self.contents.add(pit, layer=pit.layer)


        self.hazard_nodes = []
        self.enemies = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()


    # super basic method atm, designed to be expanded as needed in later iterations
    def add_player(self, player):
        self.entry_door.enter(player)
        player.move(bound_rect=self.full_rect)

    def add_players(self, players):
        for each in players:
            self.add_player(each)

    def add_enemy(self, nme):
        nme.move(bound_rect=self.full_rect)
        self.enemies.add(nme)


    def spawn_enemy(self, variety, number, **kwargs):
        ret = []
        for x in range(0, number):
            s_node = self.nodes[random.randint(0, len(self.nodes)-1)]
            ret.append(variety(s_node, node_list=self.nodes))
            self.enemies.add(ret)
        #for each in ret:
        #    self.contents.add(each, layer=each.layer)
        return ret


    def add_door(self, side, position, *args):
        if side == 'left':
            new_door = door(side_x=self.full_rect.left, pos=position, bound_y=self.full_rect.top)
        elif side == 'center':
            new_door = door(coords=self.full_rect.center)
        elif side == 'right':
            new_door = door(side_x=self.full_rect.right, pos=position, bound_y=self.full_rect.top)
        elif side == 'bottom':
            new_door = door(side_y=self.full_rect.bottom, pos=position, bound_x=self.full_rect.top)
        elif side == 'top':
            new_door = door(side_y=self.full_rect.top, pos=position, bound_x=self.full_rect.top)
        else:
            return False
        return new_door

    def add_entrance(self, side, position, *args):
        if side == 'left':
            self.full_rect.left = self.visible_rect.left
            new_door = door(events.to_hub, side_x=self.full_rect.left, pos=position, bound_y=self.full_rect.top)
        elif side == 'center':
            self.full_rect.center = self.visible_rect.center
            new_door = door(events.to_hub, coords=self.full_rect.center)
        elif side == 'right':
            self.full_rect.right = self.visible_rect.right
            new_door = door(events.to_hub, side_x=self.full_rect.right, pos=position, bound_y=self.full_rect.top)
        elif side == 'bottom':
            self.full_rect.bottom = self.visible_rect.bottom
            new_door = door(events.to_hub, side_y=self.full_rect.bottom, pos=position, bound_x=self.full_rect.left)
        elif side == 'top':
            self.full_rect.top = self.visible_rect.top
            new_door = door(events.to_hub, side_y=self.full_rect.top, pos=position, bound_x=self.full_rect.left)
        else:
            return False

        if self.full_rect.width < self.visible_rect.width:
            self.full_rect.centerx = self.visible_rect.centerx
            new_door.adjust(bound_rect=self.full_rect.inflate(100, 100))
        if self.full_rect.height < self.visible_rect.height:
            self.full_rect.centery = self.visible_rect.centery
            new_door.adjust(bound_rect=self.full_rect.inflate(100, 100))

        return new_door

    def update(self, player_one, all_players, *args, **kwargs):
        self.contents.update()

        player_one_rect = player_one.rect
        # calculates the scroll, and also sort of the counter_scroll based upon the player's position
        x, y = 0, 0
        if player_one_rect.centerx > self.scroll_rect.right:
            x = -(player_one_rect.centerx - self.scroll_rect.right)
        elif player_one_rect.centerx < self.scroll_rect.left:
            x = self.scroll_rect.left - player_one_rect.centerx
        if player_one_rect.centery > self.scroll_rect.bottom:
            y = -(player_one_rect.centery - self.scroll_rect.bottom)
        elif player_one_rect.centery < self.scroll_rect.top:
            y = self.scroll_rect.top - player_one_rect.centery

        self.scroll(x, y)
        self.counter_scroll(x, y, player_one, *all_players)
        #self.enemies.update()

    def draw_contents(self, disp, boxes=False):
        if not boxes:
            return self.contents.draw(disp)
        else:
            ret = self.contents.draw(disp)
            self.draw_boxes(disp)
            return ret

    def get_contents(self):
        return self.contents

    def draw_boxes(self, disp):
        for w in self.all_walls:
            w.draw_boxes(disp)
        for e in self.enemies:
            e.draw_boxes(disp)
        for f in self.contents.get_sprites_from_layer(doors_layer):
            f.draw_boxes(disp)
        for r in self.nodes:
            pygame.draw.rect(disp, config.default_transparency, r.rect, 4)

        self.ground.draw_boxes(disp)
        pygame.draw.rect(disp, config.green, self.full_rect, 4)
        pygame.draw.rect(disp, config.blue, self.visible_rect, 4)

    # a basic scroll everything to the [direction] method
    def scroll(self, x_scroll, y_scroll):
        for each in self.contents:
            each.move(shift=(x_scroll, y_scroll))
        for node in self.nodes:
            node.rect.move_ip(x_scroll, y_scroll)
        for each in self.enemies:
            each.move(shift=(x_scroll, y_scroll))

    def counter_scroll(self, x_scroll, y_scroll, *args):
        for each in args:
            each.move(shift=(x_scroll, y_scroll))

    def collide_walls(self, **kwargs):
        if 'obstacles' in kwargs:
            self.all_walls.add(kwargs['obstacles'])
        if 'players' in kwargs:
            # only checks the collision of the outer rect, not the hitbox.
            bonks = pygame.sprite.groupcollide(kwargs['players'], self.all_walls, False, False, collide_hitbox)
            for each in bonks:
                each.move(walls=bonks[each])
            bonks_o = pygame.sprite.groupcollide(kwargs['players'], self.hazards, False, False, collide_hitbox)
            for each in bonks_o:
                each.move(walls=bonks_o[each])
        if 'missiles' in kwargs:
            for each in kwargs['missiles']:
                if not self.visible_rect.colliderect(each.hitbox.rect):
                    each.kill()
            dead = pygame.sprite.groupcollide(kwargs['missiles'], self.all_walls, True, False, collide_hitbox)
            for each in dead:
                for every in dead[each]:
                    each.react(every)
        if 'enemies' in kwargs:
            bonks_a = pygame.sprite.groupcollide(kwargs['enemies'], self.all_walls, False, False, collide_hitbox)
            for each in bonks_a:
                each.move(walls=bonks_a[each], bound_rect=self.full_rect)
                for every in bonks_a[each]:
                    each.react(every)


    # checks collision for doors, and using some crazy nesting of for-loops, checks every player against every door
    # they're in contact with
    def collide_doors(self, players):
        if not bool(self.enemies):

            dings = pygame.sprite.groupcollide(self.contents.get_sprites_from_layer(doors_layer), players, False, False, collide_hitbox)
            for each in dings:
                for every in dings[each]:
                    each(every)

    def collide_traps(self, players):
        dings = pygame.sprite.groupcollide(self.contents.get_sprites_from_layer(doors_layer), players, False, False,
                                           collide_hitbox)
        for each in dings:
            for every in dings[each]:
                each(every)
        #trips = pygame.sprite.groupcollide(self.traps, players, False, False,
        #                                   collide_hitbox)
        #for each in trips:
        #    for every in dings[each]:
        #        each(every)

    def collide_missiles_into_enemies(self, incoming):
        dings = pygame.sprite.groupcollide(incoming, self.enemies, False, False, collide_hitbox)
        for each in dings:
            for every in dings[each]:
                each(every)

    def collide_missiles_into_players(self, incoming, players):
        pass

    def pull_enemies(self, **kwargs):
        return collections.deque(self.enemies)


class hub_room(room):
    def __init__(self, disp, my_theme=default_theme):
        super().__init__(('center', 2), (7, 5), disp, my_theme,
                         exit_door=[('top', 3),
                                    ],
                         )


class multiroom(room):
    def __init__(self, enter_from, size, theme, disp, *args, **kwargs):
        super().__init__(enter_from, size, theme, disp, *args, **kwargs)


class DEBUG_room(room):
    def __init__(self, disp, my_theme,  *args, **kwargs):
        s_x, s_y = random.randint(5, 14), random.randint(5, 14)
        super().__init__(('left', 5), (s_x, s_y), disp, my_theme, *args, **kwargs)

class boss_room(room):
    def __init__(self, disp, my_theme,  *args, **kwargs):
        s_x, s_y = random.randint(14, 24), random.randint(14, 24)
        super().__init__(('left', 5), (s_x, s_y), disp, my_theme, *args, **kwargs)

class donut_room(room):
    def __init__(self, disp, my_theme, *args, **kwargs):
        s_x, s_y = random.randint(12, 28), random.randint(12, 28)
        s_x = int(max(s_x, (s_x + s_y) / 2))
        s_y = int(max(s_y, (s_x + s_y) / 2))
        portion = random.randint(2, 5)
        print("portion=", portion)
        inner_rect = pygame.rect.Rect((int((s_x/2)*config.tile_scalar), int((s_y/2)*config.tile_scalar)),
                                      (portion*config.tile_scalar, portion*config.tile_scalar))

        super().__init__(('left', 5), (s_x, s_y), disp, my_theme, *args, **kwargs, inner_wall_rect=inner_rect)

class bridge_room(room):
    def __init__(self, disp, my_theme, *args, **kwargs):
        s_x = max(random.randint(14, 22), random.randint(12, 18))
        s_y = min(random.randint(8, 22), random.randint(6, 18))
        gap_start = random.randint(6, 10)
        gap_length = int(random.randint(4, 7))
        inner_rect = pygame.rect.Rect((gap_start*config.tile_scalar, 0),
                                      (gap_length*config.tile_scalar, s_y*config.tile_scalar))
        bridge_h = int(s_y/random.randint(2, 4))
        bridge_rect = pygame.rect.Rect((gap_start*config.tile_scalar, random.randint(0, int(s_y-bridge_h))*config.tile_scalar), (gap_length*config.tile_scalar, bridge_h*config.tile_scalar))

        super().__init__(('left', 5), (s_x, s_y), disp, my_theme, *args, **kwargs, pit_rect=inner_rect, bridge_rect=bridge_rect)


import enemies

# the dungeon class is designed to be a holder for all the stuff that we need to randomly generate a room, as well as a
# means by which we can generate new rooms
class dungeon():
    def __init__(self, difficulty, dungeon_theme, disp, *args, **kwargs):
        self.difficulty = difficulty
        self.my_theme = dungeon_theme

        event_maker.make_entry('trace', 'theme check', "assessing the contents of theme", 'room', False, False, 'theme',
                               found_theme=self.my_theme)

        self.disp = disp
        self.hub = hub_room(disp, self.my_theme)
        self.current_room = self.hub
        self.challenge = 4

    def next_room(self, players):
        self.challenge += 2
        easy_enemies = {
            0: enemies.abenenoemy,
            1: enemies.quintenemy,
            2: enemies.node_sniper,
            3: enemies.fire_spitter,

        }
        hard_enemies = {
            0: enemies.skeleton,
            1: enemies.beetle,
            2: enemies.elite_beetle,
        }
        #event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
        #                      spawn_enemy=(enemies.abenenoemy, 1)),
        #event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
        #                      spawn_enemy=(enemies.quintenemy, 3)),
        #event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
        #                      spawn_enemy=(enemies.fire_spitter, 2)),
        #event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
        #                      spawn_enemy=(enemies.node_sniper, 2))
        for x in range(0, self.challenge):
            selected = random.randint(0, 3)
            event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
                                  spawn_enemy=(easy_enemies[selected], 1)),
        for x in range(4, self.challenge):
            selected = random.randint(0, 2)
            event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
                                  spawn_enemy=(hard_enemies[selected], 1)),
        possible_rooms = {
            0: DEBUG_room,
            1: donut_room,
            2: bridge_room,
            3: boss_room,
        }
        if self.challenge <= 8:
            self.current_room = possible_rooms[random.randint(0, 2)](self.disp, self.my_theme, )
        else:
            self.current_room = possible_rooms[3](self.disp, self.my_theme, )
            event_maker.new_event(events.spriteling_event, 'room', subtype=events.spawn_enemy,
                                  spawn_enemy=(enemies.big_blue_beetle, 1)),
        #self.current_room = bridge_room(self.disp, self.my_theme, )
        #self.current_room = donut_room(self.disp, self.my_theme, )
        self.current_room.add_players(players)
        return self.current_room

    def __call__(self, *args, **kwargs):
        return self.current_room

    def get_hub(self):
        return self.hub

    def go_to_hub(self, players):
        self.current_room = self.hub
        self.current_room.add_players(players)
        return self.current_room


class basic_dungeon(dungeon):
    def __init__(self, disp):
        super(basic_dungeon, self).__init__(1, default_theme, disp)
