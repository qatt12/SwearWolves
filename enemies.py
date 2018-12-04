import pygame, spriteling, events, spells, config, blocks, random
from events import event_maker
from spells import velocity
from config import fps as sec

def can_attack(bad_guy, victim):
    return bad_guy.check_attack(victim)

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
    def __init__(self, start_node, *args, **kwargs):
        super().__init__(*args, loc=start_node.rect.center, **kwargs)
        self.layer = config.enemy_layer
        self.missiles = pygame.sprite.Group()
        if 'resists' in kwargs:
            for resistance in kwargs['resists']:
                self.base_modifiers[resistance[0]] = resistance[1]
        if 'immune_to' in kwargs:
            for immunity in kwargs['immune_to']:
                self.base_immune.add(immunity)
        if 'hp' in kwargs:
            self.base_hp = kwargs['hp']
        else:
            self.base_hp = 400
        self.spell_layer = config.spell_layer
        self.attack_box = self.hitbox

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def add(self, *args, **kwargs):
        if 'impact' in kwargs:
            self.missiles.add(kwargs['impact'])

    def attack(self):
        pass

    def check_attack(self, target):
        pass

    def get_missiles(self):
        return self.missiles

    def get_nodes(self):
        return []

class reactive_enemy(enemy):
    def __init__(self, attack_box, weapon, start_node, *args, **kwargs):
        pass

class nme_fire_bolt_s(spells.spell):
    def __init__(self, **kwargs):
        super().__init__(nme_fireball_m, spells.fire_book_img,
                         spell_name="fireball", **kwargs, trigger_method=spells.cooled(sec/4))

class nme_fireball_m(spells.missile):
    def __init__(self, dir, loc, **kwargs):
        # fsx = pygame.mixer.Sound("Music/MM.ogg")
        # pygame.mixer.Sound.play(fsx)
        super().__init__(spells.fire_ball_img, loc, velocity(mag=4, dir=dir), **kwargs, missile_name='fireball',
                         elem='fire', damage=56)

class dumb_turret(enemy):
    def __init__(self, start_node, weapon):
        super().__init__(loc=start_node.center)
        self.attack = weapon

class abenenoemy(enemy):
    def __init__(self, start_node, **kwargs):
        super().__init__(start_node, img=skull_img)
        self.my_vel   = velocity(7, 5.489874531)
        self.stuck =0
        self.x_change =False
        self.y_change =False

    def update(self, *args, **kwargs):
        super().update()
        self.rect.move_ip(self.my_vel())
        #print("Velocity: " + str(self.my_vel[0]) + ", " + str(self.my_vel[1]))
        if self.stuck>0:
            self.stuck-=1

    def react(self, to, *args, **kwargs):

        if self.stuck>0:
            if self.x_change:
                #switch x
                #print("Y needs to change")
                self.my_vel(-self.my_vel[1])
                self.stuck==0
            elif self.y_change:
                #switch y
                #print("X needs to change")
                self.my_vel(False,-self.my_vel[0])
                self.stuck==0

        #if wall to left
        if self.hitbox.rect.centerx > to.hitbox.rect.centerx:
            self.my_vel(False, -self.my_vel[1]) #go right
            self.x_change =False
            self.y_change =True
        #elif wall to right
        elif self.hitbox.rect.centerx <= to.hitbox.rect.centerx:
            self.my_vel(False, self.my_vel[1])  #go left
            self.x_change = False
            self.y_change = True

        #if wall up
        if self.hitbox.rect.centery > to.hitbox.rect.centery:
            self.my_vel(-self.my_vel[0])    #go down
            self.y_change = False
            self.x_change = True

        #if wall down
        elif self.hitbox.rect.centery < to.hitbox.rect.centery:
            self.my_vel(self.my_vel[0])     #go up
            self.y_change = False
            self.x_change = True

        self.stuck+=2
        #if to.hitbox.rect.centery ==0:
         #   self.my_vel(flip=(False,True))


        #if to.hitbox.rect.top < self.hitbox.rect.centery < to.hitbox.rect.top:
        #    self.my_vel(flip=(True, False))
        #if to.hitbox.rect.left < self.hitbox.rect.centerx < to.hitbox.rect.right:
        #    self.my_vel(flip=(False, True))


class quintenemy(enemy):
    def __init__(self, start_node, **kwargs):
        super().__init__(start_node, img=quintenemy_img)
        valid_nodes = kwargs['node_list']
        self.patrol_route = []
        for x in range(0, random.randint(2, 5)):
            self.patrol_route.append(valid_nodes[random.randint(0, len(valid_nodes)-1)])
        self.base_move = 4
        self.stop = 0
        self.dest = self.patrol_route[self.stop].rect.center

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.dest = self.patrol_route[self.stop].rect.center
        if self.rect.collidepoint(self.dest):
            self.stop += 1
            if self.stop >= len(self.patrol_route):
                self.stop = 0
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
            self.move(True, move=(x_v, y_v))

    def draw_boxes(self, disp):
        super().draw_boxes(disp)
        for each in self.patrol_route:
            pygame.draw.rect(disp, config.blue, each.rect, 2)

default_trap_img = pygame.image.load( 'Animation\img_trap.jpg')
default_trap_img= pygame.transform.scale(default_trap_img, (config.tile_scalar, config.tile_scalar))

class node_sniper(enemy):
    def __init__(self, start_node, node_list, **kwargs):
        super().__init__(start_node, img=default_trap_img)
        temp_nodes = [n for n in node_list if events.dist(n, start_node) <= 250]
        self.attack_box = temp_nodes[random.randint(0, len(temp_nodes)-1)]
        self.weapon = spells.solar_beam_s(caster=self)
        self.layer = config.floor_cos


    def check_attack(self, target):
        #print("checking collide for node sniper; target= ", target)
        #print("my attack box: ", self.attack_box.rect)
        if self.attack_box.rect.colliderect(target.hitbox.rect):
            self.snipe(target)

    def draw_boxes(self, disp):
        super().draw_boxes(disp)
        pygame.draw.rect(disp, config.blue, self.attack_box.rect, 2)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.weapon.update(True, self.rect.center, False, False, *args, **kwargs)

    #def update(self, active, loc, prev, now, *args, **kwargs):
    #    super().update(*args, **kwargs)
    #    if self.recoil > 0:
    #        self.recoil -= 1
    #    if active:
    #        self.rect.center = loc
    #        if self.my_trigger(prev, now) and 'missile_layer' in kwargs:
    #            kwargs['missile_layer'].add(self.cast(kwargs['direction']))

    def snipe(self, target):
        x_adj = self.rect.centerx - target.hitbox.rect.centerx + 0.01
        y_adj = self.rect.centery - target.hitbox.rect.centery + 0.01
        arc = x_adj/y_adj
        angle = (arc, 1)
        self.weapon.update(True, self.rect.center, True, True, direction=angle, missile_layer=self.missiles,
                           caster=self)




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