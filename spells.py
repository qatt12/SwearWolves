import spriteling, pygame
from config import fps as sec

light_wave_img = pygame.image.load(      'projectiles\img_blast.png').convert_alpha()
fire_ball_img  = pygame.image.load(   'projectiles\img_fireball.png').convert_alpha()
acid_ball_img  = pygame.image.load( 'projectiles\img_poisonball.png').convert_alpha()
icy_ball_img   = pygame.image.load(    'projectiles\img_iceball.png').convert_alpha()

basic_books    = pygame.image.load('projectiles\img_basic_books.png').convert_alpha()
ice_book_img   = basic_books.subsurface(( 0,  0), (20, 20))
fire_book_img  = basic_books.subsurface(( 0, 20), (20, 20))
acid_book_img  = basic_books.subsurface(( 0, 40), (20, 20))
light_book_img = basic_books.subsurface(( 0, 60), (20, 20))
blank_book_img = basic_books.subsurface(( 0, 60), (20, 20))


bigger_books = pygame.transform.scale2x(basic_books)
bb_size = bigger_books.get_rect()
h = bb_size.height
onfr = h/4
w = bb_size.width
big_ice_book_img   = bigger_books.subsurface(( 0, onfr*0), (w, onfr))
big_fire_book_img  = bigger_books.subsurface(( 0, onfr*1), (w, onfr))
big_acid_book_img  = bigger_books.subsurface(( 0, onfr*2), (w, onfr))
big_light_book_img = bigger_books.subsurface(( 0, onfr*3), (w, onfr))
big_blank_book_img = bigger_books.subsurface(( 0, onfr*3), (w, onfr))

# the arrangement of spells (or more generally, all attacks) goes like this: each player character gets a spell book,
# and each spell book has a particular pre-defined list of spells attached to it (one spell for each category). To
# unlock new spells, the 'add_spell' method is called from the spell book, and a string referencing the spell to be
# added is passed in. the spell_book, which already has all possible spells defined and listed in an internal
# dictionary, uses the passed in string as the key to look up which spell it should add.
# mechanically, the book just keeps track of the spells (which are unlocked and which is selected) and makes sure the
# spell's image appears in the right place (that it follows the player character around). the spell is a (potentially
# animated) sprite that follows the pc around and handles the firing of missiles/projectiles


# spell book is a handler/container class meant to hold a bunch of spells
class spell_book(spriteling.spriteling):
    def __init__(self, level):
        super().__init__(image=blank_book_img)
        print("a new spell book has been made")
        # contains an instance of/ constructor for all unlocked spells
        self.spells = []
        self.spell_key = {0: spell}
        self.level_costs = {0: 1000, 1: 2000}
        self.level = level
        self.index = 0
        self.length = 1

        # this is maintained so that spells not currently selected can still be updated (mostly fo spells that need to
        # cool down; their cooldowns don't reset upon selecting a new spell
        self.other_spells = pygame.sprite.Group()
        self.active_spell = pygame.sprite.GroupSingle()


# each attack/spell has two components: the spell and the missile. the spell is basically just an image that follows the
# player around, while the missile is created and propelled by the spell.
# 'attack' and 'spell' are nearly interchangeable, but since 'spell' technically/internally refers to a specific object
# w/i the game files, I will shy away from using it unless I'm talking about that particular object

# ancestral class for missiles (things that fly out and hit other things)
# missiles are fired (begin moving) immediately after begin created
class missile(spriteling.spriteling):
    def __init__(self, img, loc, vel):
        super().__init__(image=img, loc=loc)
        self.velocity = vel

    def update(self, *args):
        self.rect.move_ip(self.velocity)
        for each in self.hitboxes:
            each.rect.center = self.rect.center

# spells themselves don't do much, except for creating and launching missiles
# by default, spells are semi-automatic, meaning the fire key has to be released in between shots
class spell(spriteling.spriteling):
    def __init__(self, projectile, img):
        super().__init__(image=img)
        # this is to be initialized just before its time to fire
        self.projectile = projectile

    def update(self, *args, **kwargs):
        if 'loc' in kwargs:
            self.rect.center = kwargs['loc']

    def cast(self, prev, now, missile_layer, direction):
        if now and not prev:
            missile_layer.add(self.fire(direction))

    def fire(self, direction):
        return self.projectile(direction, self.rect.center)


# charge_up spells need to be charged by holding the fire button until they are sufficiently charged
# every frame in which the fire button is held (it determines if the button is held by checking the current and previous
# frame's data) the spell gains 1 charge.
class charge_up(spell):
    def __init__(self, threshold, *args):
        super().__init__(*args)
        self.charge = 0
        self.charge_time = threshold * sec

    def cast(self, prev, now, missile_layer, direction):
        if now and not prev:
            self.stage = 1
        elif now and prev:
            self.charge += 1
        elif not now and self.charge == self.charge_time:
            missile_layer.add(self.fire(direction))
            self.charge = 0
        elif prev and not now:
            self.charge =0

# multi
class multicharge(charge_up):
    def __init__(self, thresholds, *args):
        self.charge_levels = thresholds
        super().__init__(thresholds[0], *args)


class cool_down(spell):
    def __init__(self, timer, *args):
        super().__init__(*args)
        self.heat = 0
        self.cooldown_time = timer * sec

    def cast(self, prev, now, missile_layer, direction):
        if self.heat > 0:
            self.heat -=1
        if now and self.heat == 0:
            missile_layer.add(self.fire(direction))



class beam(spell):
    def __init__(self, *args):
        super().__init__(*args)
        self.own_missiles = pygame.sprite.Group()

    def update(self, loc, interface, missile_layer, *args, **kwargs):
        self.rect.center = loc
        prev, now = interface.check_fire()


class targeted(spell):
    pass


class fireball_s(spell):
    def __init__(self):
        super().__init__(fireball_m, fire_book_img)

class fireball_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, fire_ball_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))

####### DEBUG STUFF
class charged_fireball_s(charge_up):
    def __init__(self):
        super().__init__(1, fireball_m, fire_book_img)

####### END DEBUG STUFF


class iceshard_s(spell):
    def __init__(self):
        super().__init__(iceshard_m, ice_book_img)

class iceshard_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4 * dir[0], 4 * dir[1]
        missile.__init__(self, icy_ball_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


class acidic_orb_s(spell):
    def __init__(self):
        super().__init__(acidic_orb_m, acid_book_img)

class acidic_orb_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, acid_ball_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


class light_wave_s(spell):
    def __init__(self):
        super().__init__(light_wave_m, light_book_img)

class light_wave_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, light_wave_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


# the book of fire contains fire spells.
class book_of_fire(spell_book):
    def __init__(self):
        super().__init__(0)
        self.image = fire_book_img
        self.goddess_lookup_key = 'crop_top'
        self.palette_lookup_key = ('blue', 'light blue', 'sapphire')
        self.spell_key = {0: fireball_s}
        self.level_costs = {0: 1000, 1: 2000}


# the book of ice contains ice spells.
class book_of_ice(spell_book):
    def __init__(self):
        super().__init__(0)
        self.image = ice_book_img
        self.goddess_lookup_key = 'body_suit'
        self.palette_lookup_key = ('blue', 'light blue', 'sapphire')
        self.spell_key = {0: iceshard_s}
        self.level_costs = {0: 1000, 1: 2000}


# the book of acid contains acid spells.
class book_of_acid(spell_book):
    def __init__(self):
        super().__init__(0)
        self.image = acid_book_img
        self.goddess_lookup_key = 'tattered'
        self.palette_lookup_key = ('blue', 'light blue', 'sapphire')
        self.spell_key = {0: acidic_orb_s}
        self.level_costs = {0: 1000, 1: 2000}


class book_of_light(spell_book):
    def __init__(self):
        super().__init__(0)
        self.image = light_book_img

        self.goddess_lookup_key = 'robes'
        self.palette_lookup_key = ('blue', 'light blue', 'sapphire')
        self.spell_key = {0: light_wave_s}
        self.level_costs = {0: 1000, 1: 2000}