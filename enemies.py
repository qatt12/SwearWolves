import pygame, spriteling, events, spells, config, blocks
from events import event_maker
from spells import velocity

skull_img = pygame.image.load(    'Animation\img_apis.png').convert()
skull_img.set_colorkey(config.default_transparency)


class enemy(spriteling.spriteling):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = config.enemy_layer

    def attack(self):
        pass

class simple_enemy(enemy):
    def __init__(self):
        super().__init__()


    def update(self, *args, **kwargs):
        self.rect.move_ip(self.move(vel=(10, 0)))
        super().update(*args, **kwargs)



class patrol(simple_enemy):
    pass


class bouncy(simple_enemy):
    pass


class abenenoemy(enemy):
    def __init__(self, location):
        super().__init__(img=skull_img, loc=location)
        self.my_vel = velocity(10, 5.6785433451)

    def update(self, *args, **kwargs):
        super().update()
        self.rect.move_ip(self.my_vel())

    def react(self, to, *args, **kwargs):
        if self.hitbox.rect.centerx > to.hitbox.rect.centerx:
            self.my_vel(False, -self.my_vel[1])

        elif self.hitbox.rect.centerx < to.hitbox.rect.centerx:
            self.my_vel(False, self.my_vel[1])
        if self.hitbox.rect.centery > to.hitbox.rect.centery:
            self.my_vel(-self.my_vel[0])

        elif self.hitbox.rect.centery < to.hitbox.rect.centery:
            self.my_vel(self.my_vel[0])

        #if to.hitbox.rect.top < self.hitbox.rect.centery < to.hitbox.rect.top:
        #    self.my_vel(flip=(True, False))
        #if to.hitbox.rect.left < self.hitbox.rect.centerx < to.hitbox.rect.right:
        #    self.my_vel(flip=(False, True))


class quintenemy(enemy):
    def __init__(self, location, patrol_route):
        super().__init__(loc=location)

        self.base_move = 4

        self.patrol_route = patrol_route
        self.stop = 0
        self.dest = self.patrol_route[self.stop]

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.rect.collidepoint(self.dest):
            self.stop += 1
            if self.stop >= len(self.patrol_route):
                self.stop = 0
            self.dest = self.patrol_route[self.stop]
        else:
            x_v, y_v = 0, 0
            if self.rect.centerx < self.dest[0]:
                x_v += 1
            elif self.rect.centerx > self.dest[0]:
                x_v -= 1
            if self.rect.centery < self.dest[1]:
                y_v += 1
            elif self.rect.centery > self.dest[1]:
                y_v -= 1
            # LOGAN:::DEBUG inefficient, will likely change
            self.move(True, move=(x_v, y_v))


#class skeleton
#follows player; randomly chooses between multiple(?)
'''
    def __init__()
        stuff
        
    def update()
        stuff
'''

#class boss
#avoids player, spawn beetles(?)
#shoot swarms
'''
    def __init__()
        stuff

    def update()
        stuff
'''

#class beetles
#surround boss, shoot at player
'''
    def __init__()
        stuff

    def update()
        stuff
'''


class brain_storm():
    pass


class not_as_simple_enemies(enemy):
    # when this thing hits a wall
    def react(self, to, *args, **kwargs):
        if isinstance(to, blocks.block):
            self.velocity = (-self.velocity[0], -self.velocity[1])