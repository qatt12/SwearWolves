import pygame, spriteling, events, spells, config, blocks, random, math
from events import event_maker
from spells import velocity
from config import fps as sec

def can_attack(bad_guy, victim):
    return bad_guy.check_attack(victim)

skull_img = pygame.image.load(    'Animation\img_skull.png').convert()
skull_img.set_colorkey(config.default_transparency)

boss_img = pygame.image.load('Animation\img_scarab_boss.png').convert()
boss_img = boss_img.subsurface((232, 0), (115, 162))
boss_img.set_colorkey(config.default_transparency)


quintenemy_img = pygame.image.load('Animation\img_spikey.png').convert()
quintenemy_img.set_colorkey(config.default_transparency)

skele_img = pygame.image.load('Animation\img_skeleton.png').convert()
skele_img.set_colorkey(config.default_transparency)

scarab_img = pygame.image.load('Animation\img_scarab_front.png').convert()
scarab_img.set_colorkey(config.default_transparency)

scarab_swarm_img = pygame.image.load('Animation\img_swarm.png').convert()
scarab_swarm_img.set_colorkey(config.default_transparency)

super_scarab_img = pygame.image.load('Animation\img_spellcaster.png').convert()
super_scarab_img.set_colorkey(config.default_transparency)

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
        self.layer = config.enemy_layer
        self.spell_layer = config.spell_layer
        self.attack_box = self.hitbox
        self.elem = 'evil'
        self.threat = 20
        self.dmg_timer = 0
        if "dmg_cooldown" in kwargs:
            self.dmg_cooldown = kwargs['dmg_cooldown']
        else:
            self.dmg_cooldown = 10

    def draw_boxes(self, disp):
        super().draw_boxes(disp)
        pygame.draw.rect(disp, config.blue, self.attack_box.rect, 2)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if self.dmg_cooldown > 0:
            self.dmg_cooldown -= 1

    def add(self, *args, **kwargs):
        if 'impact' in kwargs:
            self.missiles.add(kwargs['impact'])

    def attack(self, target):
        if self.dmg_timer ==0:
            self.dmg_timer = self.dmg_cooldown
            target.damage(self.elem, self.threat)
        target.move(push=[self])


    def check_attack(self, target):
        if self.attack_box.rect.colliderect(target.hitbox.rect):
            self.attack(target)

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

default_trap_img = pygame.image.load( 'Animation\img_scarab.png')
default_trap_img= pygame.transform.scale(default_trap_img, (config.tile_scalar, config.tile_scalar))

# sun lazer
class solar_beam_s(spells.beam):
    def __init__(self, **kwargs):
        super().__init__(sun_particle_m, spells.leaf_book_img, **kwargs,
                         trigger_method=spells.cooled(sec*2), spell_name="solar_beam")
class sun_particle_m(spells.beam_particle):
    def __init__(self, num, prev, loc, **kwargs):
        super().__init__(num, prev, spells.sun_particle_img, loc, missile_name="sun_particle", **kwargs, damage=26)



class node_sniper(enemy):
    def __init__(self, start_node, node_list, **kwargs):
        super().__init__(start_node, img=scarab_img)
        temp_nodes = [n for n in node_list if events.dist(n, start_node) <= 250]
        self.attack_box = temp_nodes[random.randint(0, len(temp_nodes)-1)]
        self.weapon = solar_beam_s(caster=self)
        self.layer = config.floor_cos


    def check_attack(self, target):
        if self.attack_box.rect.colliderect(target.hitbox.rect):
            self.attack(target)

    def draw_boxes(self, disp):
        super().draw_boxes(disp)
        pygame.draw.rect(disp, config.blue, self.attack_box.rect, 2)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.weapon.update(True, self.rect.center, False, False, *args, **kwargs)


    def attack(self, target):
        x_adj = self.rect.centerx - target.hitbox.rect.centerx + 0.01
        y_adj = self.rect.centery - target.hitbox.rect.centery + 0.01
        x_s = math.copysign(1, x_adj)
        y_s = math.copysign(1, y_adj)
        print('x_a:', x_adj, 'y_a:', y_adj, x_s, y_s)
        if x_adj < 0:
            if x_adj < y_adj:
                print("at test")
                if x_adj > y_adj:
                    print("case 1")
                    arc = y_adj/x_adj
                    angle = (-math.copysign(arc, x_s), -y_s)
                elif x_adj < y_adj:
                    print("case 2")
                    arc = y_adj/x_adj
                    angle = (-x_s, -math.copysign(arc, y_s))
                else:
                    angle = (-1, 0)
            else:
                if x_adj > y_adj:
                    arc = x_adj/y_adj
                    angle = (-math.copysign(arc, x_s), -y_s)
                elif x_adj < y_adj:
                    arc = y_adj/x_adj
                    angle = (-x_s, math.copysign(arc, -y_s))
                else:
                    angle= (-1, 0)

        else:
            if x_adj < y_adj:
                arc = x_adj/y_adj
                angle = (-math.copysign(arc, x_s), -y_s)
            elif x_adj > y_adj:
                arc = y_adj/x_adj
                angle = (-x_s, math.copysign(arc, -y_s))
            else:
                angle= (-1, 0)
        print(angle)
        self.weapon.update(True, self.rect.center, True, True, direction=angle, missile_layer=self.missiles,
                           caster=self)

class fire_spitter(node_sniper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weapon = fire_bolt_s(caster=self)

class over_heated(spells.trigger):
    def __init__(self, max_heat, heat_per_missile):
        self.over_heated = False
        self.max_temp = max_heat
        self.buildup = heat_per_missile
        self.temp = 0

    def __call__(self, prev, now):
        if not self.over_heated and now:
            self.temp += self.buildup
            self.over_heated = self.temp > self.max_temp
            return True
        elif self.temp > 0:
            self.temp -= 1
            return False
        else:
            self.over_heated = False
        return False

class bolt_caster(node_sniper):
    def __init__(self, start_node, node_list, **kwargs):
        super().__init__(start_node, node_list, img=default_trap_img)
        self.weapon = fire_bolt_s(caster=self)
        self.layer = config.floor_cos


class fire_bolt_s(spells.spell):
    def __init__(self, **kwargs):
        super().__init__(fire_cloud_m, spells.leaf_book_img, **kwargs,
                         trigger_method=over_heated(sec*2, 24), spell_name="solar_beam")
class fire_cloud_m(spells.missile):
    def __init__(self, dir, loc, **kwargs):
        super().__init__(spells.fire_ball_img, loc, velocity(mag=3, dir=dir), **kwargs, missile_name='fireball',
                         elem='fire', damage=37, hp=7)

class active_enemy(enemy):
    def __init__(self, start_node, *args, **kwargs):
        super(active_enemy, self).__init__(start_node, *args, **kwargs)
        self.tracked_player = None
        self.attention_timer = 0
        self.reassess_targets = sec*3
        self.accuracy = 0.2
        self.sight = 350
        self.weapon = fire_bolt_s(caster=self)


    def look_for_players(self, players):
        dist = self.sight
        self.tracked_player = None
        for each in players:
            if events.dist(self, each) <= dist:
                print("found a close player")
                dist = events.dist(self, each)
                self.tracked_player = each
        return bool(self.tracked_player)

    def aim(self, target):
        x_adj = self.rect.centerx - target.hitbox.rect.centerx + 0.01
        y_adj = self.rect.centery - target.hitbox.rect.centery + 0.01
        x_s = math.copysign(1, x_adj)
        y_s = math.copysign(1, y_adj)
        #print('x_a:', x_adj, 'y_a:', y_adj, x_s, y_s)
        if x_adj < 0:
            if x_adj < y_adj:
                #print("at test")
                if x_adj > y_adj:
                    #print("case 1")
                    arc = y_adj/x_adj
                    angle = (-math.copysign(arc, x_s), -y_s)
                elif x_adj < y_adj:
                    #print("case 2")
                    arc = y_adj/x_adj
                    angle = (-x_s, -math.copysign(arc, y_s))
                else:
                    angle = (-1, 0)
            else:
                if x_adj > y_adj:
                    arc = x_adj/y_adj
                    angle = (-math.copysign(arc, x_s), -y_s)
                elif x_adj < y_adj:
                    arc = y_adj/x_adj
                    angle = (-x_s, math.copysign(arc, -y_s))
                else:
                    angle= (-1, 0)

        else:
            if x_adj < y_adj:
                arc = x_adj/y_adj
                angle = (-math.copysign(arc, x_s), -y_s)
            elif x_adj > y_adj:
                arc = y_adj/x_adj
                angle = (-x_s, math.copysign(arc, -y_s))
            else:
                angle= (-1, 0)
        #print(angle)
        x_acc = random.random() * self.accuracy
        y_acc = random.random() * self.accuracy
        #angle = (angle[0] + math.copysign(x_acc, angle[0]), angle[1] + math.copysign(y_acc, angle[1]))
        return angle

    def fire(self, angle):
        self.weapon.update(True, self.rect.center, True, True, direction=angle, missile_layer=self.missiles,
                           caster=self)

    def flee_from(self, target, dist=350):
        start_dist = events.dist(self, target)
        if start_dist <= dist:
            if self.rect.centerx < target.rect.centerx:
                self.move(True, move=(-1, 0))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(1, 0))
            if self.rect.centery < target.rect.centery:
                self.move(True, move=(0, -1))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(0, 1))
        return events.dist(self, target) > dist

    def approach(self, target, min_dist=270, max_dist=300):
        start_dist = events.dist(self, target)
        if start_dist <= max_dist:
            if self.rect.centerx < target.rect.centerx:
                self.move(True, move=(1, 0))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(-1, 0))
            if self.rect.centery < target.rect.centery:
                self.move(True, move=(0, 1))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(0, -1))
        elif start_dist <= min_dist:
            if self.rect.centerx < target.rect.centerx:
                self.move(True, move=(-1, 0))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(1, 0))
            if self.rect.centery < target.rect.centery:
                self.move(True, move=(0, -1))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(0, 1))
        return min_dist < events.dist(self, target) < max_dist

    def pursue(self, target, dist=30):
        start_dist = events.dist(self, target)
        if start_dist >= dist:
            if self.rect.centerx < target.rect.centerx:
                self.move(True, move=(1, 0))
            elif self.rect.centerx > target.rect.centerx:
                self.move(True, move=(-1, 0))
            if self.rect.centery < target.rect.centery:
                self.move(True, move=(0, 1))
            elif self.rect.centery > target.rect.centery:
                self.move(True, move=(0, -1))
        return events.dist(self, target) < dist

class slash_s(spells.wave_caster):
    def __init__(self, **kwargs):
        super().__init__(spells.swipe_img, True, swipe_thing_m, spells.rock_book_img, **kwargs,
                         #scaled=(13, 8),
                         stretched=(20, 16, 10),
                         spell_name='fissure',
                         trigger_method=over_heated(2*sec, 36),
                         recoil=((sec/8)+1))

class swipe_thing_m(spells.ground_wave):
    def __init__(self, img_set, direction, loc, *args, **kwargs):
        super().__init__(img_set, 0, loc, (direction[0]*1.7, direction[1]*1.7), *args, **kwargs, missile_name='slab',
                         stage_delay=1, start_delay=20, delay_drop=1, drop_dist=-30, hp=9, damage=15, elem='rock',
                         knockback=(direction, 2.5))
        #event_maker.new_event(events.spriteling_event, 'spells', subtype=events.spawn_obstacle, spawn_obstacle=self)

class skeleton(active_enemy):
    def __init__(self, start_node, **kwargs):
        super().__init__(start_node, img=skele_img, **kwargs)
        self.weapon = slash_s(caster=self)
        self.curr_move = 2
        self.base_hp = 1700
        self.curr_hp = 1700
        self.stalk_time = 0
        self.attack_time = 0
        self.sight = 1000
        self.idle_time = 0

    def update(self, players, *args, **kwargs):
        super().update(*args, **kwargs)
        self.weapon.update(True, self.rect.center, False, False, *args, **kwargs)
        if self.idle_time > 0:
            print("idling")
            self.idle_time -= 1
        else:
            if self.attention_timer > 0:
                self.attention_timer -= 1
            elif self.attention_timer == 0:
                print("looking for players")
                if self.look_for_players(players):
                    print("found one")
                    self.attention_timer = 4*sec
                else:
                    print("none found")
                    self.attention_timer = 2*sec
            if self.attention_timer > 0 and bool(self.tracked_player):
                dist = events.dist(self, self.tracked_player)
                if self.attack_time > 0:
                    self.attack_time -= 1
                    print("pursuing")
                    if self.pursue(self.tracked_player, 65):
                        self.fire(self.aim(self.tracked_player))
                        self.attack_time -= 1
                        self.stalk_time = 2*sec
                elif self.stalk_time > 0:
                    print("approaching")
                    self.stalk_time -= 1
                    self.approach(self.tracked_player)
                    if dist < 250:
                        self.stalk_time -= 2
                        self.attack_time = 1*sec
                elif self.idle_time > 0:
                    print("handging back")
                    if self.flee_from(self.tracked_player, 450):
                        self.idle_time -=5
                    else:
                        self.idle_time -=1
                elif dist > 550 :
                    self.stalk_time = 2
                elif dist < 60:
                    self.idle_time = 1.5*sec
                elif dist <= 550:
                    self.attack_time = 1*sec

class beetle(active_enemy):
    def __init__(self, start_node, **kwargs):
        super().__init__(start_node, img=scarab_img,  **kwargs)
        self.weapon = fire_bolt_s(caster=self)
        self.hitbox.rect = scarab_img.get_rect().inflate(-70, -20)
        self.curr_move = 2.7
        self.base_hp = 1400
        self.curr_hp = 1400
        self.stalk_time = 0
        self.attack_time = 0
        self.sight = 1000
        self.idle_time = 0
        self.melee_attack = slash_s(caster=self)


    def melee(self, angle):
        self.melee_attack.update(True, self.rect.center, True, True, direction=angle, missile_layer=self.missiles,
                           caster=self)

    def update(self, players, *args, **kwargs):
        super().update(*args, **kwargs)
        self.weapon.update(True, self.rect.center, False, False, *args, **kwargs)
        self.melee_attack.update(True, self.rect.center, False, False, *args, **kwargs)
        if self.idle_time > 0:
            print("idling")
            self.idle_time -= 1
        else:
            if self.attention_timer > 0:
                self.attention_timer -= 1
            elif self.attention_timer == 0:
                if self.look_for_players(players):
                    self.attention_timer = 4 * sec
                else:
                    self.attention_timer = 2 * sec
            if self.attention_timer > 0 and bool(self.tracked_player):
                dist = events.dist(self, self.tracked_player)
                if self.stalk_time > 0:
                    print("approaching")
                    self.stalk_time -= 1
                    if self.approach(self.tracked_player, 350, 500):
                        self.stalk_time -= 1
                        self.fire(self.aim(self.tracked_player))
                elif self.attack_time > 0:
                    self.attack_time -= 1
                    if dist > 180:
                        self.attack_time -= 1
                    print("pursuing")
                    if self.pursue(self.tracked_player, 45):
                        self.melee(self.aim(self.tracked_player))
                        self.attack_time -= 1
                        self.stalk_time = 2 * sec
                elif self.idle_time > 0:
                    print("hanging back")
                    if self.flee_from(self.tracked_player, 650):
                        self.idle_time -= 5
                    else:
                        self.idle_time -= 1
                elif dist > 150:
                    self.stalk_time = 2
                elif dist < 60:
                    self.idle_time = 1.5 * sec
                elif dist <= 550:
                    self.attack_time = 1 * sec

class elite_beetle(active_enemy):
    def __init__(self, start_node, **kwargs):
        super().__init__(start_node, img=super_scarab_img, **kwargs)
        #self.image = super_scarab_img
        self.weapon = solar_beam_s(caster=self)
        self.hitbox.rect = scarab_img.get_rect().inflate(-70, -20)

        self.curr_move = 3.8
        self.base_hp = 2000
        self.curr_hp = 2000
        self.stalk_time = 0
        self.max_stalk_time = 2 * sec
        self.attack_time = 0
        self.sight = 1000
        self.idle_time = 0
        self.melee_attack = slash_s(caster=self)

    def melee(self, angle):
        self.melee_attack.update(True, self.rect.center, True, True, direction=angle, missile_layer=self.missiles,
                           caster=self)

    def update(self, players, *args, **kwargs):
        super().update(*args, **kwargs)
        self.weapon.update(True, self.rect.center, False, False, *args, **kwargs)
        self.melee_attack.update(True, self.rect.center, False, False, *args, **kwargs)
        if self.idle_time > 0:
            print("idling")
            self.idle_time -= 1
        else:
            if self.attention_timer > 0:
                self.attention_timer -= 1
            elif self.attention_timer == 0:
                if self.look_for_players(players):
                    self.attention_timer = 4 * sec
                else:
                    self.attention_timer = 2 * sec
            if self.attention_timer > 0 and bool(self.tracked_player):
                dist = events.dist(self, self.tracked_player)
                if dist >= 250:
                    if self.attack_time > 3:
                        self.attack_time -= 3
                        self.stalk_time += 1
                elif dist < 120 and self.attack_time < 90:
                    self.attack_time += 4
                elif dist >= 120:
                    if self.attack_time > 2:
                        self.attack_time -= 2
                    self.stalk_time += 1
                    self.idle_time += 1
                if self.stalk_time > 0:
                    print("approaching")
                    self.stalk_time -= 1
                    if self.approach(self.tracked_player, 500, 700):
                        self.stalk_time -= 1
                        self.fire(self.aim(self.tracked_player))
                elif self.attack_time > 70:
                    self.attack_time -= 1
                    self.stalk_time += 4
                    if dist > 180:
                        self.attack_time -= 1
                    if dist > 400:
                        self.idle_time += 5
                    print("pursuing")
                    if self.pursue(self.tracked_player, 45):
                        self.melee(self.aim(self.tracked_player))
                        self.attack_time -= 1
                        self.stalk_time = 2 * sec
                elif self.idle_time > 0:
                    print("hanging back")
                    if self.flee_from(self.tracked_player, 700):
                        self.idle_time -= 2
                    else:
                        self.idle_time -= 1
                elif dist > 250:
                    self.stalk_time += 2
                elif dist < 60:
                    self.idle_time = 1.5 * sec
                elif dist <= 550:
                    self.stalk_time = 1 * sec

class scarab_beam_s(spells.helix):
    def __init__(self, **kwargs):
        super().__init__(scarab_beam_m, spells.ice_book_img, spell_name='ice_beam', **kwargs,
                                        trigger_method=over_heated(4, 55))

class scarab_beam_m(spells.threelix):
    def __init__(self, partner, orbital_rank, loc, direction, *args, **kwargs):
        xvel, yvel = direction[0]*5, direction[1]*5
        super().__init__(partner, 4, orbital_rank, scarab_swarm_img, loc, (xvel, yvel),

                         *args, **kwargs,
                         missile_name='ice_helix', hp=5, elem='bug', damage=40,
                         #effects=[spriteling.slow('ice', .15, 14)]
                         )

class heavy_slash_s(spells.wave_caster):
    def __init__(self, **kwargs):
        super().__init__(spells.swipe_img, True, heavy_swipe_thing_m, spells.rock_book_img, **kwargs,
                         #scaled=(13, 8),
                         stretched=(20, 16, 10),
                         spell_name='fissure',
                         trigger_method=over_heated(2.8*sec, 36),
                         recoil=((sec/8)+1))

class heavy_swipe_thing_m(spells.ground_wave):
    def __init__(self, img_set, direction, loc, *args, **kwargs):
        super().__init__(img_set, 0, loc, (direction[0]*1.7, direction[1]*1.7), *args, **kwargs, missile_name='slab',
                         stage_delay=1, start_delay=20, delay_drop=1, drop_dist=-30, hp=9, damage=18, elem='rock',
                         knockback=(direction, 2.5))

class spawn_scarab(spells.spell):
    def __init__(self, **kwargs):
        super().__init__(scarab_spawn_m, spells.DEBUG_book_img, **kwargs, trigger_method=over_heated(10*sec, 10*sec+1))
class scarab_spawn_m(spells.spawn_enemy_m):
    def __init__(self, *args, **kwargs):
        super().__init__(beetle)

class spawn_elite_scarab(spells.spell):
    def __init__(self, **kwargs):
        super().__init__(scarab_elite_spawn_m, spells.DEBUG_book_img, **kwargs, trigger_method=over_heated(20*sec, 20*sec+1))
class scarab_elite_spawn_m(spells.spawn_enemy_m):
    def __init__(self, *args, **kwargs):
        super().__init__(elite_beetle)

class big_blue_beetle(active_enemy):
    def __init__(self, start_node, **kwargs):
        super().__init__(start_node, img=boss_img, **kwargs)
        self.weapon = scarab_beam_s(caster=self)
        self.hitbox.rect = boss_img.get_rect().inflate(-50, -20)

        self.curr_move = 3.8
        self.base_hp = 3500
        self.curr_hp = 3500
        self.max_run_time = sec
        self.run_time = 0
        self.stalk_time = 0
        self.max_stalk_time = 2 * sec
        self.attack_time = 0
        self.max_attack_time = 1 * sec
        self.sight = 1000
        self.idle_time = 0
        self.melee_attack = heavy_slash_s(caster=self)
        self.accuracy = 0.15
        self.melee_delay = 0
        self.summon_a = spawn_scarab(caster=self)
        self.summon_b = spawn_elite_scarab(caster=self)
        self.summon_timer = 10

    def summon(self):
        self.summon_a.update(True, self.rect.center, True, True, direction=(0, 0), missile_layer=self.missiles,
                                 caster=self)
        self.summon_b.update(True, self.rect.center, True, True, direction=(0, 0), missile_layer=self.missiles,
                                 caster=self)
        self.missiles.update()

    def melee(self, angle):
        self.melee_attack.update(True, self.rect.center, True, True, direction=angle, missile_layer=self.missiles,
                           caster=self)

    def update(self, players, *args, **kwargs):
        super().update(*args, **kwargs)
        self.weapon.update(True, self.rect.center, False, False, *args, **kwargs)
        self.melee_attack.update(True, self.rect.center, False, False, *args, **kwargs)
        if self.idle_time > 0:
            print("idling")
            self.idle_time -= 1
        else:
            if self.attention_timer > 0:
                self.attention_timer -= 1
            elif self.attention_timer == 0:
                if self.look_for_players(players):
                    self.attention_timer = 4 * sec
                else:
                    self.attention_timer = 2 * sec
            if self.attention_timer > 0 and bool(self.tracked_player):
                dist = events.dist(self, self.tracked_player)
                if self.summon_timer > 0:
                    self.summon_timer -= 1
                    self.summon()
                if dist >= 450:
                    self.summon_timer += 1
                    if self.attack_time > 3:
                        self.attack_time -= 3
                        self.stalk_time += 1
                elif dist < 120:
                    self.attack_time += 4

                if self.stalk_time > 0:
                    print("approaching")
                    self.stalk_time -= 1
                    if self.approach(self.tracked_player, 500, 700):
                        self.stalk_time -= 1
                        self.fire(self.aim(self.tracked_player))
                elif self.attack_time > 50:
                    self.attack_time -= 1
                    if dist > 180:
                        self.attack_time -= 1
                    if dist > 400:
                        self.idle_time += 5
                    print("pursuing")
                    if self.pursue(self.tracked_player, 45):
                        self.melee(self.aim(self.tracked_player))
                        self.attack_time -= 1
                        self.stalk_time = 2 * sec
                elif self.idle_time > 0:
                    print("hanging back")
                    if self.flee_from(self.tracked_player, 700):
                        self.idle_time -= 2
                    else:
                        self.idle_time -= 1
                elif dist > 250:
                    self.stalk_time = 2
                elif dist < 60:
                    self.idle_time = 1.5 * sec
                elif dist <= 550:
                    self.stalk_time = 1 * sec

class boss(enemy):
#avoids player, spawn scarabs(?)
#shoot swarms
    def __init__(self):
        super().__init__(img=boss_img)

    #def update(self,*args,**kwargs):
    #    super().update(*args,**kwargs)
    #    #move away from player
#
    #    if "player" in kwargs:
    #        pass
    #    x_v, y_v = 0,0
    #    # if player to the left and no wall to right
    #    # move right
    #    if self.rect.centerx < player.rect.centerx:
    #        x_v -= 1
    #    # elif player to the left and wall to right
    #    # move up
    #    elif self.rect.centerx < player.rect.centerx and hits wall:
    #        y_v += 1
    #    #if player to the right and no wall to left
    #        #  move left
    #    if self.rect.centerx > player.rect.centerx:
    #        x_v += 1
    #    #elif player to the right and wall to the left
    #        # move down
    #    elif self.rect.centerx > player.rect.centerx and hits wall:
    #        y_v -= 1
    #    #if player up and no wall down
    #        # move down
    #    if self.rect.centery < player.rect.centery:
    #        y_v -= 1
    #    #elif player up and wall down
    #        # move right
    #    elif self.rect.centery < player.rect.centery and hits wall:
    #        x_v += 1
    #    #if player down and no wall up
    #        # move up
    #    if self.rect.centery > player.rect.centery:
    #        y_v += 1
    #    #elif player down and wall up
    #        # move left
    #    elif self.rect.centery > player.rect.centery and hits wall:
    #        x_v -= 1
#
#
    #    if self.timer >= config.fps*3:
    #        k = random.randint(1,3)
    #        if k is 1:
    #             #shoot at player (on a timer somehow?)
#
    #        if k is 2:
    #            #fires off swarm
    #        if k is 3:
    #            #spawn enemy(?)
    #    self.timer += 1

class scarab(enemy):
#surround boss, shoot at player
    def __init__(self):
        super().__init__(img=scarab_img)

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