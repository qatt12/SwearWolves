# rooms are a sort of container class that hold and manage their contents.
# as self-evident as the above sounds, it is an important note

import pygame, blocks, config
sGroup = pygame.sprite.Group

from blocks import wall as wall
from blocks import corner as corner
from blocks import floor as floor
from blocks import door as door
from config import tile_scalar

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
    def build_walls(self, border):
        all_walls = sGroup()
        # spawns and positions the outer wall pieces. Note the i + 50 and j + 50: this cause the wall segments to
        # slightly overlap w/ the corner segments' rects, thus properly enclosing the room
        for i in range(border.left, border.right, tile_scalar):
            all_walls.add(wall('up', self.image_lookup['tw'], (i + 50, border.top)))
            all_walls.add(wall('down', self.image_lookup['bw'], (i + 50, border.bottom)))
        for j in range(border.top, border.bottom, tile_scalar):
            all_walls.add(wall('left', self.image_lookup['lw'], (border.left, j + 50)))
            all_walls.add(wall('right', self.image_lookup['rw'], (border.right, j + 50)))

        all_walls.add(corner('top_left', self.image_lookup['tlc'], border.topleft))
        all_walls.add(corner('bottom_left', self.image_lookup['blc'], border.bottomleft))
        all_walls.add(corner('top_right', self.image_lookup['trc'], border.topright))
        all_walls.add(corner('bottom_right', self.image_lookup['brc'], border.bottomright))

        return all_walls


# the core functions of the room are to hold everything that is going to appear on the screen, check for and report the
# interactions between certain sprites, and to draw everything in the correct order
class room():
    def __init__(self, enter_from, size, theme, disp):
        # the constructor reqs a size tuple for height and width in tiles, a theme from which to draw tiles and enemies,
        # the current difficulty level, and the player's point of entry.
        self.theme = theme

        # the floor(s) are interesting. in order to allow the creation of irregularly shaped (non-rectangular) floors,
        # each segment of floor is created separately, then linked together. upon first being initialized, a room has a
        # simple, rectangular floor enclosed in a bounding wall.
        self.floors = sGroup()
        self.ground = floor(size, theme)
        self.floors.add(self.ground)

        self.all_sprites = sGroup()

        # this is supposed to help with screen scrolling for the room. The visible rect is what is currently on-screen,
        # the full rect is for the entire room
        self.visible_rect = disp.get_rect()
        self.full_rect = self.ground.rect

        if enter_from[0] == 'left':
            self.full_rect.left = self.visible_rect.left
            self.entry_door = door(side_x=self.full_rect.left, pos=enter_from[1])
        elif enter_from[0] == 'center':
            self.full_rect.center = self.visible_rect.center
            self.entry_door = door(coords=self.full_rect.center)
        elif enter_from[0] == 'right':
            self.full_rect.right = self.visible_rect.right
            self.entry_door = door(side_x=self.full_rect.right, pos=enter_from[1])

        if self.full_rect.width < self.visible_rect.width:
            self.full_rect.centerx = self.visible_rect.centerx
            self.entry_door.adjust(bound_rect=self.full_rect)
        if self.full_rect.height < self.visible_rect.height:
            self.full_rect.centery = self.visible_rect.centery
            self.entry_door.adjust(bound_rect=self.full_rect)


        self.doors = sGroup(self.entry_door)

        # the walls have to be spritelings in a group in order to properly register collision
        self.outer_walls = theme.build_walls(self.full_rect)

        self.enemies = sGroup()

        self.all_sprites.add(self.outer_walls, self.floors)


    # core methods used to draw the contents of the room onto the main display window in the appropriate order
    # the default/expected order is: floors, outer walls, inner walls, enemies, players, enemy missiles, unaligned
    # missiles, player missiles
    def draw_contents(self, disp):

        self.floors.draw(disp)
        self.outer_walls.draw(disp)
        self.doors.draw(disp)

    # super basic method atm, designed to be expanded as needed in later iterations
    def add_players(self, player):
        self.entry_door.enter(player)

    def spawn_enemy(self, *args, **kwargs):
        for each in args:
            self.enemies.add(each)

    def update(self, *args, **kwargs):
        self.outer_walls.update()


    def draw_boxes(self, disp):
        for w in self.outer_walls:
            w.draw_boxes(disp)

        self.ground.draw_boxes(disp)
        pygame.draw.rect(disp, config.green, self.full_rect, 4)
        pygame.draw.rect(disp, config.blue, self.visible_rect, 4)

    # look into subclassing groups to make a more efficient version of this
    def scroll(self, x_scroll, y_scroll):
        for each in self.all_sprites:
            each.rect = each.rect.move(x_scroll, y_scroll)

    def collide_walls(self, **kwargs):
        if 'players' in kwargs:
            # only checks the collision of the outer rect, not the hitbox.
            bonks = pygame.sprite.groupcollide(self.outer_walls, kwargs['players'], False, False)
            print(bonks)
            # for each in bonks:



class hub_room(room):
    def __init__(self, disp):
        #self.rect = pygame.rect.Rect((0, 0), (10*config.tile_scalar, 10*100))
        super().__init__(('left', 3), (10, 6), theme(), disp)

