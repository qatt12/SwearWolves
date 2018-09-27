import spriteling, pygame
from config import fps as fps

missile_sheet = pygame.image.load('projectiles\simple_missiles.png').convert_alpha()

fire_bolt_img = pygame.image.load('projectiles\img_fire_bolt.png').convert()
fire_bolt_spell_img = pygame.image.load('projectiles\img_fire_bolt_spell.png').convert()
book_of_fire_img = pygame.image.load('projectiles\img_book_of_fire.png').convert()

blank_book =  pygame.image.load('projectiles\img_book_of_fire.png').convert()

'''
frost_bolt_img = pygame.image.load("projectiles\img_frost_bolt.png")
frost_bolt_spell_img = pygame.image.load("projectiles\img_frost_bolt_spell.png")
book_of_frost_img = pygame.image.load("projectiles\img_book_of_frost.png")

lightning_bolt_img = pygame.image.load("projectiles\img_elec_bolt.png")
lightning_bolt_spell_img = pygame.image.load("projectiles\img_elec_bolt_spell.png")
electric_bookaloo_img = pygame.image.load("projectiles\img_book_of_elec.png")
'''


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
        super().__init__(image=blank_book)
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

    # attaches this book to a player
    # currently unfinished
    def give_to_player(self, user):
        self.rect.center = user.book_slot

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
    def __init__(self, projectile, img, loc):
        super().__init__(image=img, loc=loc)
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
    def __init__(self, loc):
        super().__init__(magic_m, fire_bolt_spell_img, loc)


class magic_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, fire_bolt_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


class DEBUG_book(spell_book):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.spell_key = {0: magic_s}
        self.level_costs = {0: 1000, 1: 2000}
        self.spells = [magic_s((0, 0))]


#
#
#
#
#


# charge_up spells need to be charged by holding the fire button until they are sufficiently charged
class charge_up(spell):
    def __init__(self, projectile, img, loc):
        spell.__init__(self, projectile, img, loc)
        self.charge = 0
        self.t1 = 4

    def update(self, interface, *args):
        prev, now = interface.check_fire()
        # the fire key was pressed/held this frame and the previous frame = the spell charges
        if now and prev:
            self.charge += 1
        # the spell fires
        elif prev and not now:
            # note: figure out which class handles the fire method
            self.live_missiles.add(self.fire)
        # the charging missile is created and placed into the live missiles
        elif now and not prev:
            self.anim('t0')

        if (self.charge/fps) >= self.t1:
            self.anim('t1')

    def anim(self, stage):
        pass


class cool_down(spell):
    pass


class beam(spell):
    pass


class fireball_s(spell):
    def __init__(self, loc):
        super().__init__(magic_m, fire_bolt_spell_img, loc)


class fireball_m(missile):
    def __init__(self, dir, loc):
        x_vel, y_vel = 4*dir[0], 4*dir[1]
        missile.__init__(self, fire_bolt_img, loc, (x_vel, y_vel))
        self.hitboxes.add(spriteling.hitbox(self))


# the book of fire contains fire spells.
class book_of_fire(spell_book):
    def __init__(self):
        super().__init__()
        self.image = book_of_fire_img
        self.user = None
        self.spell_key = {0: fireball_s}
        self.level_costs = {0: 1000, 1: 2000}

'''
# duh
class book_of_frost(spell_book):
    def __init__(self, user):
        super().__init__(book_of_frost_img, user.book_slot)

        # each of the elemental books contains a lookup of all the possible spells, called the spell key
        self.spell_key = {'bolt': frost_bolt_s, 'barrier': ice_wall_s}

        self.user = user
        self.spells = [frost_bolt_s]
        self.active_spell = self.spells[0](self.user.spell_slot)
        self.spell_selector = 0
        self.length = 1


class shocking_tome(spell_book):
    def __init__(self, user):
        super().__init__(electric_bookaloo_img, user.book_slot)

        # each of the elemental books contains a lookup of all the possible spells, called the spell key
        self.spell_key = {'bolt': lightning_bolt_s, 'barrier': thunder_ball_s}

        self.user = user
        self.spells = [frost_bolt_s]
        self.active_spell = self.spells[0](self.user.spell_slot)
        self.spell_selector = 0
        self.length = 1
'''
