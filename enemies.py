import pygame, spriteling, events, spells, config, blocks
from events import event_maker
from spells import velocity

skull_img = pygame.image.load(    'Animation\img_skull.png').convert()
skull_img.set_colorkey(config.default_transparency)

boss_img = pygame.image.load('Animation\img_scarab_boss.png').convert()
boss_img.set_colorkey(config.default_transparency)

quintenemy_img = pygame.image.load('Animation\img_spikey.png').convert()
quintenemy_img.set_colorkey(config.default_transparency)

skele_img = pygame.image.load('Animation\img_skeleton.png').convert()
skele_img.set_colorkey(config.default_transparency)

scarab_img = pygame.image.load('Animation\img_scarab.png').convert

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
        self.my_vel = velocity(5, 5)

    def update(self, *args, **kwargs):
        super().update()
        self.rect.move_ip(self.my_vel())

    def react(self, to, *args, **kwargs):
        #if wall to left
        if self.hitbox.rect.centerx > to.hitbox.rect.centerx:
            self.my_vel(False, -self.my_vel[1]) #go right
        #elif wall to right
        elif self.hitbox.rect.centerx < to.hitbox.rect.centerx:
            self.my_vel(False, self.my_vel[1])  #go left

        #if wall up
        if self.hitbox.rect.centery > to.hitbox.rect.centery:
            self.my_vel(-self.my_vel[0])    #go down

        #if wall down
        elif self.hitbox.rect.centery < to.hitbox.rect.centery:
            self.my_vel(self.my_vel[0])     #go up

        #if to.hitbox.rect.centery ==0:
         #   self.my_vel(flip=(False,True))


        #if to.hitbox.rect.top < self.hitbox.rect.centery < to.hitbox.rect.top:
        #    self.my_vel(flip=(True, False))
        #if to.hitbox.rect.left < self.hitbox.rect.centerx < to.hitbox.rect.right:
        #    self.my_vel(flip=(False, True))


class quintenemy(enemy):
    def __init__(self, location, patrol_route):
        super().__init__(img=quintenemy_img,loc=location)

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


class skeleton(enemy):
#follows player; randomly chooses between multiple(?)

    def __init__(self):
        super().__init__(img=skele_img)
        
    def update(self, *args, **kwargs):
        super().update(*args,**kwargs)
        #walk to player
        #attack if close


class boss(enemy):
#avoids player, spawn scarabs(?)
#shoot swarms
    def __init__(self):
        super().__init__(img=boss_img)

    def update(self,*args,**kwargs):
        super().update(*args,**kwargs)

        #move away from player
        #if player to the left and no wall to right
            # move right
        #elif player to the left and wall to right
            # move up

        #if player to the right and no wall to left
            #  move left
        #elif player to the right and wall to the left
            # move down

        #if player up and no wall down
            # move down
        #elif player up and wall down
            # move right

        #if player down and no wall up
            # move up
        #elif player down and wall up
            # move left

        #shoot at player (on a timer somehow?)
        #fires off swarm
        #spawn enemy(?)

class scarab(enemy):
#surround boss, shoot at player
    def __init__(self):
        super().__init(img=scarab_img)

    def update(self, *args, **kwargs):
        super().update(*args,**kwargs)
        #move to boss
        #attack player if close


class brain_storm():
    pass


class not_as_simple_enemies(enemy):
    # when this thing hits a wall
    def react(self, to, *args, **kwargs):
        if isinstance(to, blocks.block):
            self.velocity = (-self.velocity[0], -self.velocity[1])