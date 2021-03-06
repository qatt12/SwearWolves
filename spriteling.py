
#
# contains the inheritance structure and universal methods for spritelings, a class derived from pygame's sprite/group
# class.
#  this outlines how the various creatures and objects will relate to each other, and guarantees that certain derived
# classes will still have some version of a widely used function, even if they themselves don't really use it
# (ex: give everything a move function even if its a stationary object. thus if main tries to make a floor tile move,
# the game doesn't crash).
# also of importance, this allows the calling of isinstance() to help figure out how something should react to hitbox
# collision.

# note that this class hierarchy is tentative, and subject to potentially heavy overloading. It may not necessarily
# make a ton of sense to have things laid out this way, but......
# almost everything here is subject to being renamed or altered in some way.

import pygame, config, events, collections, random
from events import event_maker

event_maker.make_entry('log', 'spriteling loaded', 'spritelings.py has been loaded', 'spriteling')

placeholder = pygame.image.load("misc\imagesred.jpg").convert()
event_maker.make_entry('log', 'spriteling loaded', 'spritelings.py has been loaded', 'spriteling')


# the use of multiple hitbox is currently deprecated, cause its expensive and complicated, and makes all my code look
# like a twisted hell of for loops
def collide_hitbox(spritelingA, spritelingB):
    return spritelingA.check_collide(spritelingB)


# the common ancestor of all sprite-type classes. Provides universal methods and a core constructor that derived classes
# can use. also, by deriving everything from this, I don't have to type out pygame.sprite.Sprite as many times
class spriteling(pygame.sprite.Sprite):
    tracking_num = 0
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.t_num = spriteling.track_next()
        # new update: spriteling now takes kwargs, to make calling it less of a pain in the ass
        # this most basal constructor takes an image and a location, assigns the image to the sprite, builds a rectangle
        # from the image, moves the rectangle to the location, then builds a hitbox the same size as the rect, and
        # places it directly on top of the rect
        if 'image' in kwargs:
            self.image = kwargs['image']
        elif 'img' in kwargs:
            self.image = kwargs['img']
        else:
            self.image = placeholder
        self.rect = self.image.get_rect()
        if 'loc' in kwargs:
            self.loc = kwargs['loc']
            self.rect.center = self.loc

        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = 'trashboat'

        # a traits keyword, for passing specific named traits to the spriteling. These can be looked up later via a
        # look_for method
        if 'traits' in kwargs:
            self.traits = kwargs['traits']
        else:
            self.traits = []

        self.activity_state = {}

        self.layer = 0

        self.base_hp = 1000
        self.curr_hp = 1000
        self.healing = 0

        self.base_modifiers = {'dmg': 1, 'knockback': 1}
        self.applied_modifiers = dict()
        self.curr_modifiers = dict(self.base_modifiers)

        self.is_immune = 0
        self.base_immune = set()
        self.curr_immune = set()

        self.base_move = 1
        self.move_mult = 1
        self.curr_move = 1

        self.cond_queue = collections.deque([])

        # determines how fast and in which direction the spriteling will move in the current frame. update() will
        # perform the rect.move_ip using this
        self.velocity = (0, 0)

        # not sure I we should make all/most spritelings have only one hitbox by default, and just create a subclass
        # with extra
        if 'hitbox' in kwargs:
            self.hitbox = hitbox(self, rect=kwargs['hitbox'])
        else:
            self.hitbox = hitbox(self, img_rect=self.rect)

    def __str__(self):
        ret = str(self.t_num) + str(type(self)) + self.name + "rect/hitbox: " + str(self.rect) + '/' + str(self.hitbox)
        try:
            assert (isinstance(ret, str)), "you fucked up"
        except AssertionError:
            message = events.entry('error', "spriteling's __str__",
                                   "assessing return type of spriteling's conversion to string", 'spriteling')
            event_maker.send_entry(message, True, True)
        return ret

    def react(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        # movement stuff. concerns movement from controller input, getting hit with shit, etc
        # changed b/c this was the exception, not the norm

        self.rect.move_ip(self.move(**kwargs))
        self.hitbox.update()

        #for x in range(0, len(self.cond_queue)):
        #    temp = self.cond_queue.popleft()
        #    event_maker.make_entry("trace", 'resolving cond_queue', "", "spriteling", True, True)
        #    if bool(temp(self)):
        #        self.cond_queue.append(temp)

        self.curr_hp += self.healing
        self.healing = 0
        self.curr_hp = min(self.curr_hp, self.base_hp)
        if self.curr_hp <= 0:
            event_maker.new_event(events.spriteling_event, 'spriteling', subtype='death', message="a spriteling has died")
            self.kill()

    def affect(self):
        self.curr_move = self.base_move * self.move_mult
        # check base and current stats, restoring as needed
        for key in self.base_modifiers:
            if key not in self.applied_modifiers:
                self.curr_modifiers[key] = self.base_modifiers[key]
            elif key in self.applied_modifiers:
                self.curr_modifiers[key] = self.base_modifiers[key] - self.applied_modifiers[key]
        for key in self.applied_modifiers:
            if key not in self.base_modifiers:
                self.curr_modifiers[key] = 1 - self.applied_modifiers[key]
        for item in self.base_immune:
            if item not in self.curr_immune:
                self.curr_immune.add(item)


    def draw(self, disp, boxes=False):
        disp.blit(self.image, self.rect)
        if boxes:
            self.draw_boxes(disp)

    def draw_boxes(self, disp):
        pygame.draw.rect(disp, config.green, self.rect, 4)
        pygame.draw.rect(disp, config.red, self.hitbox.rect, 4)

    # minimize use of this; most of its functionality is being taken over by update
    def move(self, force_apply = False, **kwargs):
        message = events.entry('trace', 'moving', 'calling move() from spriteling', 'spriteling',
                               'move', 'movement', 'spriteling',
                               inst_src=self, obj_src=spriteling, old_vel=self.velocity, old_rect=self.rect)
        xvel, yvel = 0, 0
        if 'vel' in kwargs:
            xvel, yvel = kwargs['vel'][0], kwargs['vel'][1]
            message.modify(direct_vel=(xvel, yvel))
        if 'move' in kwargs:
            xvel = xvel + self.curr_move * kwargs['move'][0]
            yvel = yvel + self.curr_move * kwargs['move'][1]
            message.modify(ext_desc='; voluntary movement', move_vel=(xvel, yvel))
        if 'knockback' in kwargs:
            xvel = xvel + kwargs['knockback'][0] * self.curr_modifiers['knockback']
            yvel = yvel + kwargs['knockback'][1] * self.curr_modifiers['knockback']
        if 'walls' in kwargs:
            message.modify(new_desc='collided w/ walls', walls=kwargs['walls'])
            for wall in kwargs['walls']:
                if self.check_collide(wall):
                    # some creative tomfoolery with rectangles and clipping
                    # temp is the rectangle of overlap between the hitbox of the offending sprite and the hitbox of the wall
                    temp = self.hitbox.rect.clip(wall.hitbox.rect)
                    # before forcing a move either up or down, we need to see if our centerx is between the left and right
                    # bounds of the wall we've hit. if it is, then this is a top or bottom collision
                    if wall.hitbox.rect.left < self.rect.centerx < wall.hitbox.rect.right:
                        # if temp's centery is above our won centery, then the wall we are touching is above us, and we will
                        # need to move downwards (positive y) by an amount equal to the height of temp
                        if temp.centery < self.hitbox.rect.centery:
                            # move our own rect downwards
                            self.rect.move_ip(0, temp.height)
                        # basically the same as above, but now temp's height is negative, to reflect that we're moving
                        # upwards
                        elif temp.centery > self.hitbox.rect.centery:
                            self.rect.move_ip(0, -temp.height)
                    if wall.hitbox.rect.bottom > self.rect.centery > wall.hitbox.rect.top:
                        if temp.centerx > self.hitbox.rect.centerx:
                            self.rect.move_ip(-temp.width, 0)
                        elif temp.centerx < self.hitbox.rect.centerx:
                            self.rect.move_ip(temp.width, 0)
                    self.hitbox.update()

        if 'bound_rect' in kwargs:
            self.rect.clamp_ip(kwargs['bound_rect'])
        if 'to' in kwargs:
            self.rect.center = kwargs['to']
        if 'shift' in kwargs:
            self.rect.move_ip(kwargs['shift'])
            self.hitbox.rect.move_ip(kwargs['shift'])
        # basically the same thing as in wall-based occlusion, except slower
        if 'push' in kwargs:
            for squish in kwargs['push']:
                if self.check_collide(squish):
                    temp = self.hitbox.rect.clip(squish.hitbox.rect)
                    if temp.centerx > self.rect.centerx:
                        self.rect.move_ip(-2, 0)
                    elif temp.centerx < self.rect.centerx:
                        self.rect.move_ip(2, 0)
                    if temp.centery > self.rect.centery:
                        self.rect.move_ip(0, -2)
                    elif temp.centery < self.rect.centery:
                        self.rect.move_ip(0, 2)
                    if temp.center == self.rect.center:
                        sign = random.randint(0, 1)
                        dist_x, dist_y = random.randint(0, 3), random.randint(0, 3)
                        if sign == 0:
                            dist_x *= -1
                            dist_y *= -1
                        self.rect.move_ip(dist_x, dist_y)
            self.hitbox.update()

        if 'bounce' in kwargs:
            temp = self.hitbox.rect.clip(kwargs['bounce'])
            # ************************ pick up here

        event_maker.send_entry(message, False, False)

        self.velocity = (xvel, yvel)
        if force_apply:
            self.rect.move_ip(self.velocity)
            self.hitbox.update()
        return (xvel, yvel)

    def check_collide(self, target):
        return pygame.Rect.colliderect(self.hitbox.rect, target.hitbox.rect)

    def apply(self, *args):
        for each in args:
            self.cond_queue.append(each)

    # the damage and heal functions are important. As I have discovered, its kind of a bitch to try and apply damage
    # (esp damage over time) cleanly without splitting it into a method that creates a class that is appended to a deque
    def damage(self, form, amount):
        if form not in self.curr_immune:
            event_maker.make_entry('trace', 'damage', 'applying damage from spriteling', 'spriteling', False, False,
                                   'extra', 'damage', 'health')
            dmg = self.curr_modifiers['dmg'] * amount
            if form in self.curr_modifiers:
                dmg *= self.curr_modifiers[form]
            self.curr_hp -= dmg
            return True
        return False

    def heal(self, amount, duration=1, upfront=0):
        self.curr_hp += upfront
        if duration > 1:
            self.cond_queue.append(heal(amount, duration))

    @classmethod
    def track_next(cls):
        cls.tracking_num +=1
        return cls.tracking_num

class nodebox(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, **kwargs):
        super().__init__()
        self.rect = pygame.rect.Rect((x_pos, y_pos), (width, height))

# basic hitbox class. Essentially just a slightly fancier rect, that automagically maintains its position relative to
# its host (assuming you update it as frequently as you update the host)
class hitbox(pygame.sprite.Sprite):
    def __init__(self, subj, x=False, y=False, **kwargs):
        super().__init__()
        self.host = subj
        # if a rect is already specified in the constructor, it copies and uses that one
        if 'rect' in kwargs:
            self.rect = pygame.Rect.copy(kwargs['rect'])
            #self.rect.inflate_ip(-self.rect.width*0.8, -self.rect.height*0.7)
        if 'img_rect' in kwargs:
            self.rect = pygame.Rect.copy(kwargs['img_rect'])
            self.rect.inflate_ip(-self.rect.width*0.2, -self.rect.height*0.3)
        # if no rect is provided, it copies the rect of its host
        else:
            self.rect = pygame.Rect.copy(self.host.rect)
        # the rect scales to the provided x and y proportions
        if 'scale_x' in kwargs:
            xscale = kwargs['scale_x']
        else:
            xscale = 1
        if 'scale_y' in kwargs:
            yscale = kwargs['scale_y']
        else:
            yscale = 1

        self.rect.inflate_ip(xscale, yscale)

        if 'center' in kwargs:
            self.rect.center = kwargs['center']
        if 'left_side' in kwargs:
            self.rect.left = kwargs['left_side']
        if 'right_side' in kwargs:
            self.rect.right = kwargs['right_side']
        if 'bottom_side' in kwargs:
            self.rect.bottom = kwargs['bottom_side']
        if 'top_side' in kwargs:
            self.rect.top = kwargs['top_side']

        if x:
            self.rect.inflate_ip(self.rect.width*x-self.rect.width, 0)
        if y:
            self.rect.inflate_ip(0, self.rect.height*y-self.rect.height)

    def __str__(self):
        ret = "host: " + self.host.name + "| " + "Rect: " + str(self.rect)
        return ret

    # the ever crucial update method. By default, it just adjusts the hitbox to be centered on the host
    def update(self, **kwargs):
        self.rect.center = self.host.rect.center
        # everything has their hitbox centered by default?
        if 'center' in kwargs:
            self.rect.center = kwargs['center']
        if 'left_side' in kwargs:
            self.rect.left = kwargs['left_side']
        if 'right_side' in kwargs:
            self.rect.right = kwargs['right_side']
        if 'bottom_side' in kwargs:
            self.rect.bottom = kwargs['bottom_side']
        if 'top_side' in kwargs:
            self.rect.top = kwargs['top_side']

    # hitbox level collision detection
    def collide_hitbox(self, spritelingB):
        return pygame.Rect.colliderect(self.rect, spritelingB.hitbox)


# a damaging effect
class damage():
    def __init__(self, type_word, amount, duration):
        event_maker.make_entry('trace', 'damage', 'creating a new inst of the damage class', 'spriteling', False, False,
                               'extra', 'damage', 'health')
        self.type_str = type_word
        self.dmg_amount = amount
        self.duration = duration

    def __call__(self, subj):
        dmg = subj.curr_modifiers['dmg'] * self.dmg_amount
        if self.type_str in subj.curr_modifiers:
            dmg *= subj.curr_modifiers[self.type_str]
        subj.curr_hp -= dmg
        event_maker.make_entry('trace', 'damage', 'calling damage class', 'spriteling', False, False,
                               'extra', 'damage', 'health',
                               remaining_hp=subj.curr_hp)
        self.duration -= 1
        return self.duration > 0


class heal():
    def __init__(self, amount, duration=1):
        self.amount = amount
        self.duration = duration

    def __call__(self, subj):
        if self.duration > 0:
            subj.healing = max(self.amount, subj.healing)
        self.duration -= 1
        return self.duration >= 0


# slows a spriteling down by adjusting its move multiplier
class slow():
    def __init__(self, type_str, degree, duration):
        self.type_str = type_str
        self.degree = degree
        self.duration = duration

    def __call__(self, subj):
        if self.type_str in subj.curr_modifiers:
            slowed = self.degree * subj.curr_modifiers[self.type_str]
        else:
            slowed = self.degree
        subj.move_mult = max(0, subj.move_mult-slowed)


class knockback():
    def __init__(self, direction, magnitude):
        self.x_disp = direction[0] * magnitude
        self.y_disp = direction[1] * magnitude

    def __call__(self, subj):
        subj.move(True, knockback=(self.x_disp, self.y_disp))

class weaken():
    pass


class resist():
    pass


class facing_angle():
    def __init__(self, x_dir, y_dir, default=(1, 0)):
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

        self.default = default

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

    def __call__(self, new_dir_x, new_dir_y, mod=False, locked=False):
        if locked:
            return (self.x_dir, self.y_dir)
        elif mod:
            if self.x_dir == 0 and self.y_dir != 0:
                if new_dir_x > 0:
                    self.x_dir = 1
                elif new_dir_x < 0 or self.x_dir == -1:
                    self.x_dir = -1
                else:
                    self.x_dir = 1
            elif self.y_dir == 0 and self.x_dir != 0:
                if new_dir_y < 0:
                    self.y_dir = -1
                elif new_dir_y > 0 or self.y_dir == 1:
                    self.y_dir = 1
                else:
                    self.y_dir = -1
            elif self.x_dir == 0 and self.x_dir == 0:
                self.x_dir, self.y_dir = self.default[0], self.default[1]
            else:
                if self.x_dir < 0 < new_dir_x or self.x_dir > 0 > new_dir_x:
                        self.x_dir = 0
                if self.y_dir < 0 < new_dir_y or self.y_dir > 0 > new_dir_y:
                    self.y_dir = 0
        else:
            if new_dir_x == 0 == new_dir_y:
                return self.x_dir, self.y_dir
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
            if self.y_dir == 0 and self.x_dir == 0:
                self.x_dir, self.y_dir = self.default[0], self.default[1]
        return self.x_dir, self.y_dir
