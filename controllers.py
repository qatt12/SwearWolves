import pygame, events
from events import event_maker

deadzone = 0.15
pygame.joystick.init()


# this method is supposed to be called early on in the main method. It will check all available joysticks, hopefully
# initialize them, and return them to main.
def prepare_joysticks():
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    event_maker.make_entry("trace", 'joysticks', "preparing joysticks", 'controllers')
    print("joysticks: ", joysticks)
    return joysticks


# this method takes a joystick, and returns a properly initialized controller. it automagically determines what type of
# joystick it has been passed. Currently it can distinguish between joysticks that are Xbox One controllers, and
# joysticks that are not Xbox One controllers. The former is treated as an Xbox 360 controller.
# note that the current usage of this method within main does not allow for the use of a keyboard.
def auto_assign(x):
    if 'Xbox One' in x.get_name():
        return xbone_gamepad(x)
    elif 'Xbox 360' in x.get_name():
        return xb360_gamepad(x)
    elif pygame.key.get_pressed()[pygame.K_SPACE]:
        return keyboard()
    else:
        return other_gamepad(x)


'''
for the xbone controller:
AXES
left stick (x,y) = (0,1)
right stick (x,y) = (4,3)
left trigger = 2
right trigger = -2

BUTTONS
A = 0
B = 1
X = 2
Y = 3
left bumper = 4
right bumper = 5
Select = 6
Start = 7
left stick = 8
right stick = 9
'''

class xbone_gamepad(object):
    def __init__(self, jub):
        # I am unsure why, but I seemed to have named this controller jub
        self.jub = jub
        self.jub.init()
        #print(jub.get_name())

        self.sticks = {'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                       'RX': self.jub.get_axis(4), 'RY': self.jub.get_axis(3)}
        self.triggers = jub.get_axis(2)
        self.buttons = {'A': jub.get_button(0), 'B': jub.get_button(1),
                        'X': jub.get_button(2), 'Y': jub.get_button(3),
                        'LB': jub.get_button(4), 'RB': jub.get_button(5),
                        'Start': jub.get_button(7), 'Select': jub.get_button(6),
                        'LStick': jub.get_button(8), 'RStick': jub.get_button(9)}

        self.new_sticks = {'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                           'RX': self.jub.get_axis(4), 'RY': self.jub.get_axis(3)}
        self.new_triggers = jub.get_axis(2)
        self.new_buttons = {'A': jub.get_button(0), 'B': jub.get_button(1),
                            'X': jub.get_button(2), 'Y': jub.get_button(3),
                            'LB': jub.get_button(4), 'RB': jub.get_button(5),
                            'Start': jub.get_button(7), 'Select': jub.get_button(6),
                            'LStick': jub.get_button(8), 'RStick': jub.get_button(9)}


    # the way jub works is like this: he gathers all the controller input once per frame and saves it to himself (when
    # first created, he saves that frame's input twice). at the start of each frame, the previous frame's new input is
    # saved to (old) input, and this frame's new input is collected. Thus, jub maintains two frame's worth of input.
    # doing it this way is important because it allows the game to check for when buttons are pressed and held or
    # pressed and then released

    def update(self):
        self.buttons = self.new_buttons
        self.sticks = self.new_sticks
        self.triggers = self.new_triggers

        self.new_buttons = {
                               'A': self.jub.get_button(0), 'B': self.jub.get_button(1),
                               'X': self.jub.get_button(2), 'Y': self.jub.get_button(3),
                               'LB': self.jub.get_button(4), 'RB': self.jub.get_button(5),
                               'Start': self.jub.get_button(7), 'Select': self.jub.get_button(6),
                               'LStick': self.jub.get_button(8), 'RStick': self.jub.get_button(9)
                            }
        self.new_sticks = {'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                           'RX': self.jub.get_axis(4), 'RY': self.jub.get_axis(3)}

        # the triggers are special, in that they are not 2 separate axes, but instead the signed difference between
        #  both triggers as a single axis. If RT is pressed, axis 2 is
        self.new_triggers = self.jub.get_axis(2)

    # returns the old and new input states for a single button (this allows button mapping at the player level)
    def pull_button(self, button_name):
        return self.buttons[button_name], self.new_buttons[button_name]

    def pull_sticks(self):
        return self.sticks, self.new_sticks

    def pull_triggers(self):
        rt, lt, nrt, nlt = False, False, False, False
        if self.triggers > 0.5:
            lt = True
        elif self.triggers < -0.5:
            rt = True
        if self.new_triggers > 0.5:
            nlt = True
        elif self.new_triggers < -0.5:
            nrt = True
        return rt or nrt, lt or nlt


    def pull_face(self, **kwargs):
        ret = {'fire': self.pull_button('X'),
               'interact': self.pull_button('Y'),
               'accept': self.pull_button('A'),
               'back': self.pull_button('B'),
               'start': self.pull_button('Start'),
               'select': self.pull_button('Select'),
               'lock_next': self.pull_button('RStick'),
               'lock_prev': self.pull_button('LStick')}
        return ret

    def pull_selectors(self, **kwargs):
        ret = {'prev': self.pull_button('LB'),
               'next': self.pull_button('RB'),
               'select': 9,
               'lock_aim': self.pull_triggers()[0],
               'adj_aim': self.pull_triggers()[1]
               }
        return ret

    def pull_movement(self):
        mov_x, mov_y, dir_x, dir_y = 0, 0, 0, 0
        if abs(self.sticks['LX']) > deadzone:
            mov_x = self.sticks['LX']
        if abs(self.sticks['LY']) > deadzone:
            mov_y = self.sticks['LY']
        if abs(self.sticks['RX']) > deadzone:
            dir_x = self.sticks['RX']
        if abs(self.sticks['RY']) > deadzone:
            dir_y = self.sticks['RY']
        #if self.new_sticks["LX"]:
            #print("newStciks: ", self.new_sticks["LX"])
        # hopefully, this will eliminate controller flick
        # commented out for now, as it broke the game. Live with controller flick
        '''if self.new_sticks['LX'] !=0 and\
                self.new_sticks['LX']/abs(self.new_sticks['LX']) != self.sticks['LX']/abs(self.sticks['LX']):
            print("detected flick on LX")
            mov_x = 0
        if self.new_sticks['LY'] !=0 and\
                self.new_sticks['LY'] / abs(self.new_sticks['LY']) != self.sticks['LY'] / abs(self.sticks['LY']):
            print("detected flick on LY")
            mov_y = 0'''
        ret = {'move': (mov_x, mov_y),
               'look': (dir_x, dir_y),
               'lock_look': self.pull_triggers()[0],
               'mod_look': self.pull_triggers()[1]}
        return ret

    def check_status(self):
        if self.new_buttons['Start'] or self.buttons['Start']:
            return True
        else:
            return False


# after extensive testing, i have discovered that xbox 360 controllers are almost exactly the same as xbox one
# controllers, the only real difference that I found is that 360 controllers have the ability to represent both triggers
# being pulled at the same time
'''
for the xb360 controller:
AXES
left stick (x,y) = (0,1)
right stick (x,y) = (4,3)
left trigger = 2
right trigger = -2
BOTH right AND left trigger = axis 2 will read approx -3

BUTTONS
A = 0
B = 1
X = 2
Y = 3
left bumper = 4
right bumper = 5
Select = 6
Start = 7
left stick = 8
right stick = 9
'''
class xb360_gamepad(object):
    def __init__(self, jub):
        # I am unsure why, but I seemed to have named this controller jub
        self.jub = jub
        self.jub.init()
        #print(jub.get_name())

        self.sticks = {'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                       'RX': self.jub.get_axis(4), 'RY': self.jub.get_axis(3)}
        self.triggers = jub.get_axis(2)
        self.buttons = {'A': jub.get_button(0), 'B': jub.get_button(1),
                        'X': jub.get_button(2), 'Y': jub.get_button(3),
                        'LB': jub.get_button(4), 'RB': jub.get_button(5),
                        'Start': jub.get_button(7), 'Select': jub.get_button(6),
                        'LStick': jub.get_button(8), 'RStick': jub.get_button(9)}

        self.new_sticks = {'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                           'RX': self.jub.get_axis(4), 'RY': self.jub.get_axis(3)}
        self.new_triggers = jub.get_axis(2)
        self.new_buttons = {'A': jub.get_button(0), 'B': jub.get_button(1),
                        'X': jub.get_button(2), 'Y': jub.get_button(3),
                        'LB': jub.get_button(4), 'RB': jub.get_button(5),
                        'Start': jub.get_button(7), 'Select': jub.get_button(6),
                        'LStick': jub.get_button(8), 'RStick': jub.get_button(9)}


    # the way jub works is like this: he gathers all the controller input once per frame and saves it to himself (when
    # first created, he saves that frame's input twice). at the start of each frame, the previous frame's new input is
    # saved to (old) input, and this frame's new input is collected. Thus, jub maintains two frame's worth of input.
    # doing it this way is important because it allows the game to check for when buttons are pressed and held or
    # pressed and then released

    def update(self):
        self.buttons = self.new_buttons
        self.sticks = self.new_sticks
        self.triggers = self.new_triggers

        self.new_buttons = {
                               'A': self.jub.get_button(0), 'B': self.jub.get_button(1),
                               'X': self.jub.get_button(2), 'Y': self.jub.get_button(3),
                               'LB': self.jub.get_button(4), 'RB': self.jub.get_button(5),
                               'Start': self.jub.get_button(7), 'Select': self.jub.get_button(6),
                               'LStick': self.jub.get_button(8), 'RStick': self.jub.get_button(9)
                            }
        self.new_sticks = {
                               'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                               'RX': self.jub.get_axis(4), 'RY': self.jub.get_axis(3)
        }

        # the triggers are special, in that they are not 2 separate axes, but instead the signed difference between
        #  both triggers as a single axis. If RT is pressed, axis 2 is
        self.new_triggers = self.jub.get_axis(2)

    # returns the old and new input states for a single button (this allows button mapping at the player level)
    def pull_button(self, button_name):
        return self.buttons[button_name], self.new_buttons[button_name]

    def pull_sticks(self):
        return self.sticks, self.new_sticks

    def pull_triggers(self):
        rt, lt, nrt, nlt = False, False, False, False
        if self.triggers > 0.5:
            lt = True
        elif self.triggers < -0.5:
            rt = True
        if self.new_triggers > 0.5:
            nlt = True
        elif self.new_triggers < -0.5:
            nrt = True
        return rt or nrt, lt or nlt


    def pull_face(self, **kwargs):
        ret = {'fire': self.pull_button('X'),
               'interact': self.pull_button('Y'),
               'accept': self.pull_button('A'),
               'back': self.pull_button('B'),
               'start': self.pull_button('Start'),
               'select': self.pull_button('Select'),
               'lock_next': self.pull_button('RStick'),
               'lock_prev': self.pull_button('LStick')}
        return ret

    def pull_selectors(self, **kwargs):
        ret = {'prev': self.pull_button('LB'),
               'next': self.pull_button('RB'),
               'select': 9,
               'adj_aim': self.pull_triggers()[1],
               'lock_aim': self.pull_triggers()[0]
               }
        return ret

    def pull_movement(self):
        mov_x, mov_y, dir_x, dir_y = 0, 0, 0, 0
        if abs(self.sticks['LX']) > 0.1:
            mov_x = self.sticks['LX']
        if abs(self.sticks['LY']) > 0.1:
            mov_y = self.sticks['LY']
        if abs(self.sticks['RX']) > 0.1:
            dir_x = self.sticks['RX']/abs(self.sticks['RX'])
        if abs(self.sticks['RY']) > 0.1:
            dir_y = self.sticks['RY']/abs(self.sticks['RY'])
        ret = {'move': (mov_x, mov_y),
               'look': (dir_x, dir_y),
               'lock_look': self.pull_triggers()[0],
               'mod_look': self.pull_triggers()[1]}
        return ret

    def check_status(self):
        if self.new_buttons['Start'] or self.buttons['Start']:
            return True
        else:
            return False


class other_gamepad(xb360_gamepad):
    def __init__(self, jub):
        # I am unsure why, but I seemed to have named this controller jub
        self.jub = jub
        self.jub.init()
        #print(jub.get_name())

        self.sticks = {
            'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
            'RX': self.jub.get_axis(2), 'RY': self.jub.get_axis(3)
        }
        self.triggers = \
            jub.get_axis(5), jub.get_axis(4)
        self.trigger_btns = \
            jub.get_button(6), jub.get_button(7)
        self.buttons = {
             'A': jub.get_button(1), 'B': jub.get_button(2),
             'X': jub.get_button(0), 'Y': jub.get_button(3),
             'LB': jub.get_button(4), 'RB': jub.get_button(5),
             'Start': jub.get_button(9), 'Select': jub.get_button(8),
             'LStick': jub.get_button(10), 'RStick': jub.get_button(11)
        }

        self.new_sticks = {
            'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
            'RX': self.jub.get_axis(2), 'RY': self.jub.get_axis(3)
        }
        self.new_triggers = \
            jub.get_axis(5), jub.get_axis(4)
        self.new_trigger_btns = \
            jub.get_button(6), jub.get_button(7)
        self.new_buttons = {
            'A': jub.get_button(1), 'B': jub.get_button(2),
             'X': jub.get_button(0), 'Y': jub.get_button(3),
             'LB': jub.get_button(4), 'RB': jub.get_button(5),
             'Start': jub.get_button(9), 'Select': jub.get_button(8),
             'LStick': jub.get_button(10), 'RStick': jub.get_button(11)
        }

    def update(self):
        self.buttons = self.new_buttons
        self.sticks = self.new_sticks
        self.triggers = self.new_triggers

        self.new_buttons = {
                               'A': self.jub.get_button(1), 'B': self.jub.get_button(2),
                               'X': self.jub.get_button(0), 'Y': self.jub.get_button(3),
                               'LB': self.jub.get_button(4), 'RB': self.jub.get_button(5),
                               'Start': self.jub.get_button(9), 'Select': self.jub.get_button(8),
                               'LStick': self.jub.get_button(10), 'RStick': self.jub.get_button(11)
                            }
        self.new_sticks = {
                               'LX': self.jub.get_axis(0), 'LY': self.jub.get_axis(1),
                               'RX': self.jub.get_axis(2), 'RY': self.jub.get_axis(3)
        }

        # the triggers are special, in that they are not 2 separate axes, but instead the signed difference between
        #  both triggers as a single axis. If RT is pressed, axis 2 is
        self.new_triggers = self.jub.get_axis(5), self.jub.get_axis(4)


# super basice keyboard class for keyboard input. like the controllers, it stores two frames of input
class keyboard():
    def __init__(self):
        self.jub = dummy()
        self.key = pygame.key.get_pressed()
        self.new_key = pygame.key.get_pressed()
        self.shift_held = False
        self.shift_released = True

    def update(self):
        # print("keyboard update")
        self.key = self.new_key
        self.new_key = pygame.key.get_pressed()

    def check_status(self):
        if self.key[pygame.K_SPACE] or self.new_key[pygame.K_SPACE]:
            return True
        else:
            return False

    def pull_key(self, key_name):
        lookup = {'a': pygame.K_e,
                  'b': pygame.K_e,
                  'c': pygame.K_e,
                  'd': pygame.K_e
                  }

    def pull_face(self, **kwargs):
        ret = {'fire': (self.key[pygame.K_f], self.new_key[pygame.K_f]),
               'interact': (self.key[pygame.K_e], self.new_key[pygame.K_e]),
               'accept': (self.key[pygame.K_SPACE], self.new_key[pygame.K_SPACE]),
               'back': (self.key[pygame.K_1], self.new_key[pygame.K_1]),
               'start': (self.key[pygame.K_SPACE], self.new_key[pygame.K_SPACE]),
               'select': (self.key[pygame.K_TAB], self.new_key[pygame.K_TAB])}
        return ret

    def pull_selectors(self, **kwargs):
        index = 9
        if self.key[pygame.K_1]:
            index = 0
        elif self.key[pygame.K_2]:
            index = 1
        elif self.key[pygame.K_3]:
            index = 2
        elif self.key[pygame.K_4]:
            index = 3
        elif self.key[pygame.K_5]:
            index = 4
        elif self.key[pygame.K_6]:
            index = 5
        elif self.key[pygame.K_7]:
            index = 6
        elif self.key[pygame.K_8]:
            index = 7
        elif self.key[pygame.K_9]:
            index = 8
        # print("checking old e key", self.key[pygame.K_e])
        # print("checking new e key", self.new_key[pygame.K_e])
        return {'next': (self.key[pygame.K_e], self.new_key[pygame.K_e]),
               'prev': (self.key[pygame.K_q], self.new_key[pygame.K_q]),
               'select': index,
               'lock_aim': (self.key[pygame.K_LSHIFT], self.key[pygame.K_LSHIFT]),
               'lock_feet': (self.key[pygame.K_LCTRL], self.key[pygame.K_LCTRL])}

    def pull_movement(self, **kwargs):
        mov_x, mov_y, dir_x, dir_y = 0, 0, 0, 0
        if self.key[pygame.K_a]:
            mov_x = -1
        elif self.key[pygame.K_d]:
            mov_x = 1
        if self.key[pygame.K_w]:
            mov_y = -1
        elif self.key[pygame.K_s]:
            mov_y = 1

        if self.key[pygame.K_LEFT]:
            dir_x = -1
        elif self.key[pygame.K_RIGHT]:
            dir_x = 1
        if self.key[pygame.K_DOWN]:
            dir_y = -1
        elif self.key[pygame.K_UP]:
            dir_y = 1

        ret = {'move': (mov_x, mov_y),
               'look': (dir_x, dir_y)}
        return ret

class dummy():
    def __init__(self):
        self.id = 9808797
    def get_id(self):
        return self.id


def controller_tester():
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for each in joysticks:
        each.init()
        print("buttons: ", each.get_numbuttons())
        print("hats: ", each.get_numhats())
        print("axes: ", each.get_numaxes())
    return joysticks[0]
