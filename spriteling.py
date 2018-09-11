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

import pygame


# the common ancestor of all sprite-type classes. Provides universal methods and a core constructor that derived classes
# can use. also, by deriving everything from this, I don't have to type out pygame.sprite.Sprite as many times
class spriteling(pygame.sprite.Sprite):
    def __init__(self, img, loc):
        pygame.sprite.Sprite.__init__(self)
        # this most basal constructor takes an image and a location, assigns the image to the sprite, builds a rectangle
        #  from the image, moves the rectangle to the location, then builds a hitbox the same size as the rect, and
        # places it directly on top of the rect
        self.image = img
        self.loc = loc
        self.rect = self.image.get_rect()
        self.rect.center = (loc[0], loc[1])
        self.hitbox = pygame.Rect.copy(self.rect)
        self.hitbox.clamp(self.rect)

    def interact(self, other):
        # empty/default method to govern the behavior of this spriteling in reaction to other.
        pass


class active(spriteling):
    def __init__(self, *args):
        super().__init__(*args)


class passive(spriteling):
    def __init__(self, *args):
        super().__init__(*args)


class reactive(spriteling):
    def __init__(self, *args):
        super().__init__(*args)


# class for stationary objects that are placed and then never moved.
class block(reactive):
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


# triggers are a special class that does almost nothing until acted upon (triggered)
class trigger(reactive):
    pass



class player(active):
    pass


# enemies
class enemy(active):
    pass


# missiles, like spells, are not just projectiles. Instead, think of these as the hitboxes and particle effects
# accompanying an attack of some sort. missiles are created and deployed by spells.
class missile(active):
    pass


# shinies are basically just environmental decorations that have some animation, usually just an idle animation
class shiny(passive):
    pass


# despite being referred to as a spell, spell just indicates an attack of some sort, whether it be
# melee, ranged, or even a shield/defensive move.
# a spell proper acts as a root/core/dispenser of the actual projectiles (missile class objects)
# a case can be made that spells are more passive than reactive, since they do next to nothing except follow their
# caster around and serve as a visual indication of what missile/attack is about to happen. Furthermore, colliding
# directly with the actual spell (and NOT the missile) doesn't really do anything.
class spell(reactive):
    pass
