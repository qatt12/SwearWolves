# blocks are, as stated in the spriteling file, intended to be placed and then never moved. With the notable exception
# of floors, blocks are also supposed to impede movement

import spriteling, pygame, config

# Straight up copy-pasted this stuff from my earlier project. it should work in here with limited modificcations

class wall(spriteling.block):
    def __init__(self, facing, *args):
        super(wall, self).__init__(*args)
        #hitbox_lookup = {'up': , 'down': , 'left': ,'right': }
        self.facing = facing
        self.damage = 0
        if facing == 'up':
            self.hitbox = self.rect.inflate(0, -(self.rect.height*.65))
            self.hitbox.top = self.rect.top
        elif facing == 'down':
            self.hitbox = self.rect.inflate(0, -(self.rect.height * .65))
            self.hitbox.bottom = self.rect.bottom
        elif facing == 'left':
            self.hitbox = self.rect.inflate(-(self.rect.width*0.65), 0)
            self.hitbox.left = self.rect.left
        elif facing == 'right':
            self.hitbox = self.rect.inflate(-(self.rect.width*0.65), 0)
            self.hitbox.right = self.rect.right


# this is for inward facing/concave corners.
class corner(spriteling.block):
    def __init__(self, facing, *args):
        super().__init__(*args)
        self.hitbox = self.rect.inflate(-(self.rect.width * 0.5), -(self.rect.height*0.5))
        if facing == 'top_left':
            self.hitbox.top = self.rect.top
            #self.hitbox.bottom = self.rect.bottom
            self.hitbox.left = self.rect.left
            #self.hitbox.right = self.rect.right
        elif facing == 'top_right':
            self.hitbox.top = self.rect.top
            #self.hitbox.bottom = self.rect.bottom
            #self.hitbox.left = self.rect.left
            self.hitbox.right = self.rect.right
        elif facing == 'bottom_right':
            #self.hitbox.top = self.rect.top
            self.hitbox.bottom = self.rect.bottom
            #self.hitbox.left = self.rect.left
            self.hitbox.right = self.rect.right
        elif facing == 'bottom_left':
            #self.hitbox.top = self.rect.top
            self.hitbox.bottom = self.rect.bottom
            self.hitbox.left = self.rect.left
            #self.hitbox.right = self.rect.right

# the floor sprite is bit tricky, as it creates a rectangular floor of the size specified and sets it as its image
# this is intended to be treated as the main image/surface of a/the room
class floor(spriteling.block):
    def __init__(self, size, theme, *args):
        # passes dummy params to the parent class
        super().__init__(theme.image_lookup['f'], (0, 0))
        size_x, size_y = size[0], size[1]
        self.image = pygame.Surface((size_x * config.tile_scalar, size_y * config.tile_scalar))

        for y in range(0, size_y+1):
            for x in range(0, size_x+1):
                self.image.blit(theme.image_lookup['f'], (x * config.tile_scalar, y * config.tile_scalar))
                print('blitting a floor', "x = ", x, "y = ", y)

        self.rect = self.image.get_rect()

        print(self.rect)


