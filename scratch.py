
class test():
    def __init__(self):
        print('initializing')

    def __call__(self, x):
        print('calling with', x)

class new_test():
    def __init__(self, x):
        self.x = x
        print('at new_test: self.x = ', x)

        self.sel = self.sub_test

    def run_test(self):
        print('running w/', self.sel(self.x))

    class sub_test():
        def __init__(self, x):
            print('calling sub_test', x)

    class sub_test2():
        def __init__(self, y):
            print('calling sub_test2', y)


class new_test2(new_test):
    def __init__(self, x):
        super().__init__(x)
        self.tList = [self.sub_test]

    def show(self):
        print(self.tList)

    def add(self, new_entry):
        self.tList.append(new_entry)

def kwargs_test(x, **kwargs):
    print('start w/ x = ', x)
    if 'new' in kwargs:
        x = kwargs['new']
    print('end w/ x = ', x)

import pygame
pygame.init()

class tsprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def __str__(self):
        return self.name

testsprite1 = tsprite('#1')
testsprite2 = tsprite('#2')
print("TestSprite1: ", testsprite1)
print("testsprite2: ", testsprite2)

testgroupsingle = pygame.sprite.GroupSingle(testsprite1)
print("t0: ", testgroupsingle)
for each in testgroupsingle:
    print("each at t0: ", each)

testgroupsingle.add(testsprite2)
print("t1: ", testgroupsingle)
for each in testgroupsingle:
    print("each at t1:", each)



import events
t0 = events.new_event(1, "test", True, console_msg="Test_Event")
print(t0)

td = {'brug': 56}

def tprint(tdict, **kwargs):
    for each in tdict:
        print(each, tdict[each])
    if 'brug' in kwargs:
        print(kwargs['brugs'])

tprint(td)

def argstest(default=0, *args):
    if default:
        print(default)
    for each in args:
        print(each)

argstest('th', 'afsadf')