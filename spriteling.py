# contains the inheritance structure and universal methods for spritelings, a class derived from pygame's sprite/group
# class.
#  this outlines how the various creatures and objects will relate to each other, and guarantees that certain derived
# classes will still have some version of a widely used function, even if they themselves don't really use it
# (ex: give everything a move function even if its a stationary object. thus if main tries to make a floor tile move,
# the game doesn't crash).
# also of importance, this allows the calling of isinstance() to help figure out how something should react to hitbox
# collision

# note that this class hierarchy is tentative, and subject to potentially heavy overloading. It may not necessarily
# make a ton of sense to have things laid out this way, but......
# almost everything here is subject to being renamed or altered in some way.

import pygame, config


# the common ancestor of all sprite-type classes. Provides universal methods and a core constructor that derived classes
# can use. also, by deriving everything from this, I don't have to type out pygame.sprite.Sprite as many times
class spriteling(pygame.sprite.Sprite):
    def __init__(self, img, loc):
        super().__init__()
        # this most basal constructor takes an image and a location, assigns the image to the sprite, builds a rectangle
        #  from the image, moves the rectangle to the location, then builds a hitbox the same size as the rect, and
        # places it directly on top of the rect
        self.image = img
        self.loc = loc
        self.rect = self.image.get_rect()
        self.rect.center = (loc[0], loc[1])
        # not sure I we should make all/most spritelings have only one hitbox by default, and just create a subclass
        # with extra
        self.hitboxes = pygame.sprite.Group()

    def interact(self, other):
        # empty/default method to govern the behavior of this spriteling in reaction to other.
        pass

    def draw_boxes(self, disp):
        pygame.draw.rect(disp, config.green, self.rect, 4)
        for each in self.hitboxes:
            pygame.draw.rect(disp, config.red, each.rect, 4)


# basic hitbox class, designed to be contained in a group stored by a spriteling
class hitbox(pygame.sprite.Sprite):
    def __init__(self, subj, **kwargs):
        super().__init__()
        self.host = subj
        # if a rect is already specified in the constructor, it copies and uses that one
        if 'rect' in kwargs:
            self.rect = pygame.Rect.copy(kwargs['rect'])
        # if no rect is provided, it copies the rect of its host
        else:
            self.rect = pygame.Rect.copy(self.host.rect)

        # the rect scales to the provided x and y proportions
        if 'scale_x' in kwargs:
            xscale = kwargs['scale_x']
            print("found x_scale= ", xscale)
        else:
            xscale = 1
        if 'scale_y' in kwargs:
            yscale = kwargs['scale_y']
        else:
            yscale = 1

        self.rect.inflate_ip(xscale, yscale)
        print("inflated a rect ", self.rect)

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

    # the ever crucial update method. By default, it just adjusts the hitbox to be centered on the host
    def update(self, **kwargs):
        self.rect.center = self.host.rect.center
        # straight up copy-pasted from the init method, because why bother saving this to the hitbox when nearly
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



# class for stationary objects that are placed and then never moved.
class block(spriteling):
    def __init__(self, *args):
        super().__init__(*args)
        # if the block is rooted, it is attached to a fixed location; an (x, y) tuple
        self.rooted = None

        # if this block is linked, then it is attached to another spriteling, and thus positions its own rect relative
        # to where its link is
        self.link = None
        # the link direction. the first int is how far to the left (negative) or right (positive) of its
        # link this block is, and the second is how far above (negative) or below (positive)
        # (0,0) means that this block's center will always be matched to its link's center, and a +/-1 in either field
        # indicates that this block is attached to the inner side/edge of its link. +/-2 indicates an attachment
        # to the outer edge
        self.link_dir = (0, 0)

    # roots the block in place
    def place(self, root_loc):
        self.rooted = root_loc

    # attaches/links the block to another
    def attach(self, link, dir):
        self.link = link
        self.link_dir = dir

    # for blocks the update method simply returns them to their designated positions
    def update(self, *args):
        if self.rooted:
            self.rect.center = self.rooted
        elif self.link:
            x, y = self.link_dir[0], self.link_dir[1]
            if x == 0 and y == 0:
                self.rect.center = self.link.rect.center
            else:
                if x == 2:
                    self.rect.right = self.link.rect.left
                elif x == 1:
                    self.rect.left = self.link.rect.left
                elif x == 0:
                    self.rect.centerx = self.link.rect.centerx
                elif x == -1:
                    self.rect.right = self.link.rect.right
                elif x == -2:
                    self.rect.left = self.link.rect.right

                if y == 2:
                    self.rect.top = self.link.rect.bottom
                elif y == 1:
                    self.rect.bottom = self.link.rect.bottom
                elif y == 0:
                    self.rect.centery = self.link.rect.centery
                elif y == -1:
                    self.rect.top = self.link.rect.top
                elif y == -2:
                    self.rect.bottom = self.link.rect.top
