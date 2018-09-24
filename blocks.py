# blocks are, as stated in the spriteling file, intended to be placed and then never moved. With the notable exception
# of floors, blocks are also supposed to impede movement

import spriteling, pygame, config


# Straight up copy-pasted this stuff from my earlier project. it should work in here with limited modificcations
class wall(spriteling.block):
    def __init__(self, facing, *args):
        super(wall, self).__init__(*args)
        self.facing = facing
        self.damage = 0
        if facing == 'down':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_y=-65, bottom_side=self.rect.bottom))
        elif facing == 'top':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_y=-65, top_side=self.rect.top))
        elif facing == 'left':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_x=-65, left_side=self.rect.left))
        elif facing == 'right':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_x=-65, right_side=self.rect.right))


# this is for inward facing/concave corners.
class corner(spriteling.block):
    def __init__(self, facing, *args):
        super().__init__(*args)

        if facing == 'top_left':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_x=-50, scale_y=-50,
                                                top_side=self.rect.top, left_side=self.rect.left))
        elif facing == 'top_right':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_x=-50, scale_y=-50,
                                                top_side=self.rect.top, right_side=self.rect.right))
        elif facing == 'bottom_right':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_x=-50, scale_y=-50,
                                                bottom_side=self.rect.bottom, right_side=self.rect.right))
        elif facing == 'bottom_left':
            self.hitboxes.add(spriteling.hitbox(self,
                                                scale_x=-50, scale_y=-50,
                                                bottom_side=self.rect.bottom, left_side=self.rect.left))


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


