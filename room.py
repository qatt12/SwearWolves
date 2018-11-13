# rooms are a sort of container class that hold and manage their contents.
# as self-evident as the above sounds, it is an important note

import pygame, blocks, config, random, events
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
        floor = pygame.image.load('walls\cobble.png').convert_alpha()
        tlcrnr = pygame.image.load("walls\cnr_stn_tl.png").convert_alpha()
        trcrnr = pygame.image.load("walls\cnr_stn_tr.png").convert_alpha()
        blcrnr = pygame.image.load("walls\cnr_stn_bl.png").convert_alpha()
        brcrnr = pygame.image.load("walls\cnr_stn_br.png").convert_alpha()
        topWall = pygame.image.load("walls\wal_stn_t.png").convert_alpha()
        btmWall = pygame.image.load('walls\wal_stn_b.png').convert_alpha()
        rgtWall = pygame.image.load('walls\wal_stn_r.png').convert_alpha()
        lftWall = pygame.image.load('walls\wal_stn_l.png').convert_alpha()
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


default_theme = theme()

events.event_maker.make_entry('log', 'default_theme', 'Testing default theme construction/initialization', 'room', True, False, 'theme', 'init', 'DEBUG', obj_src=default_theme, image_lookup=default_theme.image_lookup)

# the core functions of the room are to hold everything that is going to appear on the screen, check for and report the
# interactions between certain sprites, and to draw everything in the correct order
class room():
    def __init__(self, enter_from, size, disp, my_theme, *args, **kwargs):
        # the constructor reqs a size tuple for height and width in tiles, a theme from which to draw tiles and enemies,
        # the current difficulty level, and the player's point of entry.
        self.image = pygame.Surface(size)

        self.all_sprites = sGroup()
        self.exits = sGroup()
        self.enemies = sGroup()
        self.floors = sGroup()

        # the floor(s) are interesting. in order to allow the creation of irregularly shaped (non-rectangular) floors,
        # each segment of floor is created separately, then linked together. upon first being initialized, a room has a
        # simple, rectangular floor enclosed in a bounding wall.
        self.ground = floor(size, my_theme)
        self.floors.add(self.ground)

        # this is supposed to help with screen scrolling for the room. The visible rect is what is currently on-screen,
        # the full rect is for the entire room
        self.visible_rect = disp.get_rect()
        self.full_rect = self.ground.rect
        self.scroll_rect = self.visible_rect.inflate(-150, -150)
        self.scroll_rect.center = self.visible_rect.center

        self.entry_door = self.add_entrance(enter_from[0], enter_from[1])
        if "exit_door" in kwargs:
            print("exit_door = ", kwargs['exit_door'])
            for each in kwargs['exit_door']:
                print("exit_door each= ", each)
                self.exits.add(self.add_door(each[0], each[1]))

        self.doors = sGroup(self.entry_door, self.exits)

        # the walls have to be spritelings in a group in order to properly register collision
        self.outer_walls = my_theme.build_walls(self.full_rect, enter_from, self.entry_door)

        print("door rect at init: ", self.entry_door.rect)
        self.all_sprites.add(self.outer_walls, self.floors, self.doors, self.enemies)

    # core methods used to draw the contents of the room onto the main display window in the appropriate order
    # the default/expected order is: floors, outer walls, inner walls, enemies, players, enemy missiles, unaligned
    # missiles, player missiles
    def draw_contents(self, disp, boxes=False):
        self.floors.draw(disp)
        self.outer_walls.draw(disp)
        self.doors.draw(disp)
        self.enemies.draw(disp)
        if boxes:
            self.draw_boxes(disp)

    # super basic method atm, designed to be expanded as needed in later iterations
    def add_player(self, player):
        self.entry_door.enter(player)
    def add_players(self, players):
        for each in players:
            self.add_player(each)

    def spawn_enemy(self, *args, **kwargs):
        for each in args:
            self.enemies.add(each)

    def add_door(self, side, position, *args):
        if side == 'left':
            new_door = door(side_x=self.full_rect.left, pos=position)
        elif side == 'center':
            new_door = door(coords=self.full_rect.center)
        elif side == 'right':
            new_door = door(side_x=self.full_rect.right, pos=position)
        elif side == 'bottom':
            new_door = door(side_y=self.full_rect.bottom, pos=position)
        elif side == 'top':
            new_door = door(side_y=self.full_rect.top, pos=position)
        else:
            return False
        return new_door

    def add_entrance(self, side, position, *args):
        if side == 'left':
            self.full_rect.left = self.visible_rect.left
            new_door = door(side_x=self.full_rect.left, pos=position)
        elif side == 'center':
            self.full_rect.center = self.visible_rect.center
            new_door = door(coords=self.full_rect.center)
        elif side == 'right':
            self.full_rect.right = self.visible_rect.right
            new_door = door(side_x=self.full_rect.right, pos=position)
        elif side == 'bottom':
            self.full_rect.bottom = self.visible_rect.bottom
            new_door = door(side_y=self.full_rect.bottom, pos=position)
        elif side == 'top':
            self.full_rect.top = self.visible_rect.top
            new_door = door(side_y=self.full_rect.top, pos=position)
        else:
            return False

        if self.full_rect.width < self.visible_rect.width:
            self.full_rect.centerx = self.visible_rect.centerx
            new_door.adjust(bound_rect=self.full_rect.inflate(100, 100))
        if self.full_rect.height < self.visible_rect.height:
            self.full_rect.centery = self.visible_rect.centery
            new_door.adjust(bound_rect=self.full_rect.inflate(100, 100))

        return new_door

    def update(self, player_one_rect, all_players, *args, **kwargs):
        self.outer_walls.update()
        self.doors.update()

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
        self.counter_scroll(x, y, all_players)

        # makes sure that all the sprites in the room are a part of all_sprites
        self.all_sprites.add(self.outer_walls, self.floors, self.doors, self.enemies)

    def draw_boxes(self, disp):
        for w in self.outer_walls:
            w.draw_boxes(disp)
        for e in self.enemies:
            e.draw_boxes(disp)
        for f in self.doors:
            f.draw_boxes(disp)

        self.ground.draw_boxes(disp)
        pygame.draw.rect(disp, config.green, self.full_rect, 4)
        pygame.draw.rect(disp, config.blue, self.visible_rect, 4)

    # a basic scroll everything to the [direction] method
    def scroll(self, x_scroll, y_scroll):
        for each in self.all_sprites:
            each.move(shift=(x_scroll, y_scroll))

    def counter_scroll(self, x_scroll, y_scroll, subjects):
        for each in subjects:
            each.move(shift=(x_scroll, y_scroll))

    def collide_walls(self, **kwargs):
        if 'players' in kwargs:
            # only checks the collision of the outer rect, not the hitbox.
            bonks = pygame.sprite.groupcollide(kwargs['players'], self.outer_walls, False, False, collide_hitbox)
            for each in bonks:
                each.move(walls=bonks[each])

    # checks collision for doors, and using some crazy nesting of for-loops, checks every player against every door
    # they're in contact with
    def collide_doors(self, players):
        dings = pygame.sprite.groupcollide(self.doors, players, False, False, collide_hitbox)
        for each in dings:
            for every in dings[each]:
                each(every)

    def collide_enemies(self, player):
        pass

    def pull_enemies(self, visible=False, **kwargs):
        ret = sGroup()
        if visible:
            for each in self.enemies:
                if self.visible_rect.contains(each.hitbox):
                    ret.add(each)
        else:
            ret.add(self.enemies)
        return ret


class hub_room(room):
    def __init__(self, disp, my_theme=default_theme):
        super().__init__(('left', 2), (20, 20), disp, my_theme, exit_door=[('top', 3), ('bottom', 66), ('right', 0)])


class multiroom(room):
    def __init__(self, enter_from, size, theme, disp, *args, **kwargs):
        super().__init__(enter_from, size, theme, disp, *args, **kwargs)

class DEBUG_room(room):
    def __init__(self, disp, my_theme, *args, **kwargs):
        s_x, s_y = random.randint(5, 30), random.randint(5, 30)
        super().__init__(('left', 5), (s_x, s_y), disp, my_theme, *args, **kwargs)

# the dungeon class is designed to be a holder for all the stuff that we need to randomly generate a room, as well as a
# means by which we can generate new rooms
class dungeon():
    def __init__(self, difficulty, dungeon_theme, num_players, disp, *args, **kwargs):
        self.difficulty = difficulty
        self.my_theme = dungeon_theme

        events.event_maker.make_entry('trace', 'theme check', "assessing the contents of theme", 'room', False, False, 'theme', found_theme=self.my_theme)

        self.disp = disp
        self.hub = hub_room(disp, self.my_theme)
        self.current_room = self.hub

    def next_room(self, players):
        self.current_room = DEBUG_room(self.disp, self.my_theme)
        self.current_room.add_players(players)
        return self.current_room

    def __call__(self, *args, **kwargs):
        return self.current_room

    def get_hub(self):
        return self.hub

class basic_dungeon(dungeon):
    def __init__(self, disp):
        super(basic_dungeon, self).__init__(1, default_theme, 1, disp)
