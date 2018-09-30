import spriteling, pygame
from config import fps as fps

light_wave_img = pygame.image.load('projectiles\img_blast.png').convert_alpha()
fire_ball_img = pygame.image.load('projectiles\img_fireball.png').convert_alpha()
acid_ball_img = pygame.image.load('projectiles\img_poisonball.png').convert_alpha()
icy_ball_img = pygame.image.load('projectiles\img_iceball.png').convert_alpha()

basic_books = pygame.image.load('projectiles\img_basic_books').convert_alpha()
ice_book_img = basic_books.subsurface((0, 0), (18, 18))
fire_book_img = basic_books.subsurface((36, 0), (18, 18))
acid_book_img = basic_books.subsurface((54, 0), (18, 18))
light_book_img = basic_books.subsurface((72, 0), (18, 18))
blank_book_img = basic_books.subsurface((72, 0), (18, 18))

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
    def __init__(self):
        super().__init__(image=blank_book_img)
        # contains an instance of/ constructor for all unlocked spells
        self.spells = []
        self.spell_key = {0: spell}
        self.level_costs = {0: 1000, 1: 2000}
        self.level = 0

        # selection stuff
        self.index = 0
        self.length = 1

        # this is maintained so that spells not currently selected can still be updated (mostly fo spells that need to
        # cool down; their cooldowns don't reset upon selecting a new spell
        self.other_spells = pygame.sprite.Group()

    def get_spell(self, interface):
        if interface.next_spell():
            if self.index < len(self.spells)-1:
                self.index += 1
            else:
                self.index = 0
        elif interface.prev_spell():
            if self.index == 0:
                self.index -= 1
            else:
                self.index = len(self.spells)
        return self.spells[self.index]

# each attack/spell has two components: the spell and the missile. the spell is basically just an image that follows the
# player around, while the missile is created and propelled by the spell.
# 'attack' and 'spell' are nearly interchangeable, but since 'spell' technically/internally refers to a specific object
# w/i the game files, I will shy away from using it unless I'm talking about that particular object

# spells themselves don't do much, except for creating and launching missiles
# by default, spells are semi-automatic, meaning the fire key has to be released in between shots
class spell(spriteling.spriteling):
    def __init__(self, projectile, img):
        super().__init__(image=img)
        # this is to be initialized just before its time to fire
        self.projectile = projectile

    def update(self, loc, interface, missile_layer, *args):
        self.rect.center = loc
        prev, now = interface.check_fire()
        if now and not prev:
            missile_layer.add(self.fire(interface.direction))

    def fire(self, direction):
        return self.projectile(direction, self.rect.center)

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

#  ___       _____
# |    \    |   __|
# | |\  \   |  |__
# | |/  /   |  |__
# |____/    |_____|

class magic_s(spell):
    def __init__(self):
        super().__init__(magic_m, fire_ball_img)


class magic_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, light_wave_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


class DEBUG_book(spell_book):
    def __init__(self):
        super().__init__()
        self.spell_key = {0: magic_s}
        self.level_costs = {0: 1000, 1: 2000}
        self.spells = [magic_s()]
        self.index = 0


#
#
#
#
#


# charge_up spells need to be charged by holding the fire button until they are sufficiently charged
class charge_up(spell):
    pass

class cool_down(spell):
    pass


class beam(spell):
    pass


class fireball_s(spell):
    def __init__(self):
        super().__init__(fireball_m, fire_ball_img)


class fireball_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, fire_ball_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


class iceshard_s(spell):
    def __init__(self):
        super().__init__(magic_m, ice_book_img)

class iceshard_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4 * dir[0], 4 * dir[1]
        missile.__init__(self, icy_ball_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))



# the book of fire contains fire spells.
class book_of_fire(spell_book):
    def __init__(self):
        super().__init__()
        self.image = fire_book_img
        self.spell_key = {0: fireball_s}
        self.level_costs = {0: 1000, 1: 2000}

# the book of ice contains ice spells.
class book_of_ice(spell_book):
    def __init__(self):
        super().__init__()
        self.image = ice_book_img
        self.spell_key = {0: iceshard_s}
        self.level_costs = {0: 1000, 1: 2000}

# the book of acid contains acid spells.
class book_of_acid(spell_book):
    def __init__(self):
        super().__init__()
        self.image = book_of_fire_img
        self.spell_key = {0: fireball_s}
        self.level_costs = {0: 1000, 1: 2000}