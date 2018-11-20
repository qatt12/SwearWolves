# targeted spells attach directly to a particular spriteling. They are very different from most other spells because
# they immediately instantiate their projectile, and then keep track of it, a primary target, and a list of valid
# secondary targets
class targeted(spell):
    def __init__(self, crosshair, *args, **kwargs):
        super().__init__(*args, type_name='targeted ', **kwargs)
        self.valid_targets = deque()
        self.seen = set()
        self.chosen_target = None

        # the reticle is an instance of (not a functor for) this spell's projectile
        self.reticle = crosshair()

        # targeted spells can be limited by any combination of charge up, cooldown, or wind up, depending on what is
        # passed in
        self.heat = 0
        self.charge = 0
        self.spin = 0
        if 'cooldown' in kwargs:
            self.cooldown_time = kwargs['cooldown'] * sec
        else:
            self.cooldown_time = 0
        if 'charge' in kwargs:
            self.charge_time = kwargs['charge'] * sec
        else:
            self.charge_time = -1
        if 'wind_up' in kwargs:
            self.wind_up = kwargs['wind_up'] * sec
        else:
            self.wind_up = -1
        # if none of the three fire limiters are passed in, the various limits are set to values that will always return
        # true.

        # a gate var that determines if we should still be printing the reticle to the window
        self.alive = False

    # the overloaded version of update for targeted spells is very different from most spells.
    def update(self, active, loc, prev, now, *args, **kwargs):
        self.rect.center = loc
        if self.heat > 0:
            self.heat -= 1
        if active:
            self.assess_targets(**kwargs)
            self.chosen_target = self.valid_targets.pop()
        else:
            self.charge = 0
            self.alive = False
            self.reticle.kill()
        if self.charge >= self.charge_time and self.heat == 0 and self.spin >= self.wind_up \
                and 'missile_layer' in kwargs:
            self.cast(prev, now, kwargs['missile_layer'])

    def cast(self, prev, now, layer):
        pass

    def assess_targets(self, *args, **kwargs):
        pass

class target_enemies(targeted):
    # goes thru all viable targets and assigns first, second, and third targeting params
    def assess_targets(self, *args, **kwargs):
        for arg in args:
            if arg not in self.seen:
                self.valid_targets.append(arg)
                self.seen.add(arg)
        if 'enemies' in kwargs:
            if len(kwargs['enemies']) < 0:
                self.valid_targets.clear()
                self.reticle.kill()
            for each in kwargs['enemies']:
                if each not in self.seen:
                    self.valid_targets.append(each)
                    self.seen.add(each)
                for every in self.seen:
                    if every not in kwargs['enemies']:
                        self.seen.remove(every)
        else:
            self.valid_targets.clear()





class heal_s(targeted):
    def __init__(self):
        super().__init__(targ_heal_m, light_book_img, spell_name='heal')




class targ_heal_m(missile):
    def __init__(self):
        super(targ_heal_m, self).__init__(default_reticle, (0, 0), (0, 0))

class curse_s(targeted):
    def __init__(self):
        super().__init__(targ_curse_m, light_book_img, spell_name='curse')


class targ_curse_m(missile):
    def __init__(self):
        super(targ_curse_m, self).__init__(default_reticle, (0, 0), (0, 0))

class arc(targeted):
    def __init__(self, distance, duration, frequency, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_range = distance
        self.draw_me = True
        self.timer_tip = duration
        self.timer = 0

    def draw(self, disp, boxes=False):
        #print("Calling arc.draw")
        #disp.blit(self.image, self.rect)
        super().draw(disp, boxes)
       # if self.draw_me:
        #print("should be drawing the line")
        pygame.draw.line(disp, config.purple, self.rect.center, self.reticle.rect.center, 10)

        y1_var = random.randint(0, 70)
        if y1_var % 2 ==0:
            pass

        x1 = random.randint(min(self.rect.centerx, self.reticle.rect.centerx), max(self.rect.centerx, self.reticle.rect.centerx))
        y1 = random.randint(min(self.rect.centery, self.reticle.rect.centery), max(self.rect.centery, self.reticle.rect.centery))
        if self.rect.centerx > self.reticle.rect.centerx:
            x1 = self.rect.centerx - x1
        else:
            x1 = self.rect.centerx + x1
        if self.rect.centery < self.reticle.rect.centery:
            y1 = self.rect.centery - y1
        else:
            y1 = self.rect.centery + y1
        pygame.draw.lines(disp, config.purple, False, (self.rect.center, (x1, y1), self.reticle.rect.center), 10)


class arc_DEBUG_s(arc):
    def __init__(self):
        super(arc_DEBUG_s, self).__init__(400, 0.2, 5, targ_curse_m(), targ_curse_m, fire_book_img, spell_name='arc_DEBUG')