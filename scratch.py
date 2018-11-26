
import events
from events import event_maker

class nested_functor_test():
    def __init__(self):
        self.hp = 100
#        self.damage = self.damage(self)
        self.stack = []

    class damage():
        def __init__(self, amt):
            self.amount = amt

        def __call__(self, subj):
            subj.hp -= self.amount

    def apply(self, effect):
        self.stack.append(effect)

    def update(self):
        for each in self.stack:
            each(self)

    def __str__(self):
        return str(self.hp)

class damage():
    def __init__(self, amt):
        self.amount = amt/2
    def __call__(self, subj):
        subj.hp -= self.amount

class outside():
    def __init__(self):
        self.dmg = 10
    def __call__(self, subj):
        subj.apply(subj.damage(self.dmg))

jeff = nested_functor_test()
print(jeff)
ext = outside()
ext(jeff)
jeff.update()
print(jeff)
ext(jeff)
jeff.update()
print(jeff)


def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice

@do_twice
def say_whee():
    print("Whee!")

print(type(say_whee()))


import pygame
t1 = pygame.rect.Rect((0, 0), (10, 10))
print("center= ", t1.center)
t1.move_ip(0.1, 0)
print("new center= ", t1.center)
t1.move_ip(0.9, 0)
print("new new center= ", t1.center)


x = 0.9
print(int(x+0.5))
y = 0.3
print(int(y+.5))