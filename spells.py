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
class spell_book(spriteling.spriteling):
    def __init__(self, *args):
        super().__init__(*args)
        self.spells = []
        self.spell_key = []
        self.length = 0
        self.spell_selector = 0

    # spell_book is never supposed to exist on its own, only as part of a derived class, thus the below methods
    # reference vars that a plain spell book would lack

    # repositions the active spell to be on the user's spell_slot
    def update(self, *args):
        self.active_spell.rect.center = self.user.spell_slot
        self.active_spell.update(self.user.interface)

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
    def add_spell(self, new_spell):
        if new_spell.name is any in self.spell_key:
            self.spells.append(new_spell)


# each attack/spell has two components: the spell and the missile. the spell is basically just an image that follows the
# player around, while the missile is created and propelled by the spell.
# 'attack' and 'spell' are nearly interchangeable, but since 'spell' technically/internally refers to a specific object
# w/i the game files, I will shy away from using it unless I'm talking about that particular object

# spells themselves don't do much, except for creating and launching missiles
# by default, spells are semi-automatic, meaning the fire key has to be released in between shots
class spell(spriteling.spriteling):
    def __init__(self, projectile, img, loc):
        super().__init__(img, loc)
        # this is a functor, to be initialized just before its time to fire
        self.projectile = projectile
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.live_missiles = pygame.sprite.Group()

    def update(self, interface, *args):
        prev, now = interface.check_fire()
        if now and not prev:
            self.projectile(blank_img, self.rect.center)

    def fire(self):
        pass


class charge_up(spell):
    def __init__(self, projectile, img, loc):
        spell.__init__(self, projectile, img, loc)
        self.charge = 0

    def update(self, interface, *args):
        prev, now = interface.check_fire()
        # the fire key was pressed/held this frame and the previous frame = the spell charges
        if now and prev:
            self.charge += 1
        # the spell fires
        elif prev and not now:
            # note: figure out which class handles the fire method
            self.fire()
        # the charging missile is created and placed into the live missiles
        elif now and not prev:
            self.live_missiles.add(self.projectile(self))


class cool_down(spell):
    pass

class beam(spell):
    pass


# ancestral class for missiles (things that fly out and hit other things)
class missile(spriteling.spriteling):
    def __init__(self, img, loc):
        super().__init__(self, img, loc)
        self.status = 'standby'



class fireball_s():
    pass


# the book of fire contains fire spells.
class book_of_fire(spell_book):
    def __init__(self, user):
        super().__init__(book_of_fire_img, user.book_slot)

        self.palette = 'red'

        # each of the elemental books contains a list of all the spells valid for this spellbook, called the spell key
        self.spell_key = ['fireball', 'firewall']

        self.user = user
        self.spells = [fireball_s]
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

