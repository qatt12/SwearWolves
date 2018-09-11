'''
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




t2 = new_test(new_test.sub_test)
t2.run_test()

class new_test2(new_test):
    def __init__(self, x):
        super().__init__(x)
        self.tList = [self.sub_test]

    def show(self):
        print(self.tList)

    def add(self, new_entry):
        self.tList.append(new_entry)

t3 = new_test2(5)
print('before: ')
t3.show()
t3.add(t3.sub_test2)
print('after: ')
t3.show()



def kwargs_test(x, **kwargs):
    print('start w/ x = ', x)
    x = kwargs['new_x']
    print('end w/ x = ', x)

var = 1

kwargs_test(var, old = 4)
'''
import pygame

pygame.init()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def assign_player_one(joysticks):
    for each in joysticks:
        if 'Xbox One' in each.get_name():
            return each
        elif 'Xbox 360' in each.get_name():
            return each

test_p1 = assign_player_one(joysticks)
print(test_p1.get_name())

test_p1.init()

running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass

        n = test_p1.get_numaxes()
        print('n= ', n)

        for x in range(0, n):
            if test_p1.get_axis(x):
                print("pressing axes number: ", x, test_p1.get_axis(x))