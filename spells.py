import spriteling, pygame

missile_sheet = pygame.image.load('projectiles\simple_missiles.png').convert_alpha()

fire_bolt_img = pygame.image.load('projectiles\img_fire_bolt.png').convert()
fire_bolt_spell_img = pygame.image.load('projectiles\img_fire_bolt_spell.png').convert()
book_of_fire_img = pygame.image.load('projectiles\img_book_of_fire.png').convert()

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
class spell_book(spriteling.passive):
    def __init__(self, *args):
        super().__init__(*args)
        self.spells = []

    # spell_book is never supposed to exist on its own, only as part of a derived class, thus the below methods
    # reference vars that a plain spell book would lack

    # repositions the active spell to be on the user's spell_slot
    def update(self, *args):
        self.active_spell.rect.center = self.user.spell_slot

    # returns the active spell (intended for use in conjunction with the draw method of room)
    def check_active_spell(self):
        return self.active_spell

    def next_spell(self):
        if self.spell_selector == self.length - 1:
            self.spell_selector = 0
        else:
            self.spell_selector += 1

        # this is supposed to delete the old active spell once it is no longer selected.
        # self.active_spell = None

        self.active_spell = self.spells[self.spell_selector](self.user.spell_slot)

    # unlocking a new spell in the book is done by passing a string into this method.
    def add_spell(self, spell_name):
        self.spells.append(self.spell_key[spell_name])


# each attack/spell has two components: the spell and the missile. the spell is basically just an image that follows the
# player around, while the missile is created and propelled by the spell.
# 'attack' and 'spell' are nearly interchangeable, but since 'spell' technically/internally refers to a specific object
# w/i the game files, I will shy away from using it unless I'm talking about that particular object

# spells themselves don't do much, except for creating and launching missiles
class spell(spriteling.passive):
    def __init__(self, projectile, img, loc):
        super().__init__(img, loc)
        self.projectile = projectile


# ancestral class for missiles (things that fly out and hit other things)
class missile(spriteling.active):
    def __init__(self, img, loc):
        super().__init__(img, loc)


########################################################################################################################
#                       Bolts                                                                                          #
########################################################################################################################
# most basic projectile. just travels in a straight line
class bolt(missile):
    def __init__(self, dir, *args):
        super().__init__(*args)
        self.vel_mult = 4


# the missile version of fire bolt (the part that actually travels towards and hits the enemy)
class fire_bolt_m(bolt):
    def __init__(self, *args):
        super().__init__(fire_bolt_img, *args)


# the spell version of fire bolt (just follows the player around and discharges the fire bolt missile)
class fire_bolt_s(spell):
    def __init__(self, *args):
        super().__init__(fire_bolt_m, fire_bolt_spell_img, *args)


# the missile version of frost bolt (the part that actually travels towards and hits the enemy)
class frost_bolt_m(bolt):
    def __init__(self, *args):
        super().__init__(frost_bolt_img, *args)


# the spell version of frost bolt (just follows the player around and discharges the frost bolt missile)
class frost_bolt_s(spell):
    def __init__(self, *args):
        super().__init__(frost_bolt_m, frost_bolt_spell_img, *args)


class lightning_bolt_m(bolt):
    def __init__(self, *args):
        super().__init__(frost_bolt_img, *args)


class lightning_bolt_s(spell):
    def __init__(self, *args):
        super().__init__(lightning_bolt_m, lightning_bolt_spell_img, *args)

########################################################################################################################
#                       Barriers                                                                                       #
########################################################################################################################



class barrier(missile):
    def __init__(self, *args):
        super().__init__(*args)


class fire_wall_s(spell):
    pass


class fire_wall_m(barrier):
    pass




# the book of fire contains fire spells.
class book_of_fire(spell_book):
    def __init__(self, user):
        super().__init__(book_of_fire_img, user.book_slot)

        self.palette = 'red'

        # each of the elemental books contains a lookup of all the possible spells, called the spell key
        self.spell_key = {'bolt': fire_bolt_s, 'barrier': fire_wall_s}

        self.user = user
        self.spells = [fire_bolt_s]
        self.active_spell = self.spells[0](self.user.spell_slot)
        self.spell_selector = 0
        self.length = 1


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


# a special super book containing the powers of all four lesser spell books! for use in single player
class super_book(spell_book):
    def __init__(self, user):
        super().__init__(super_book_img, user.book_slot)


