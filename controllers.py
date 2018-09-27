import pygame

deadzone = 0.3

# this method is supposed to be called early on in the main method. It will check all available joysticks, hopefully
# initialize them, and return them to main.
def prepare_joysticks():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
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
    else:
        return xb360_gamepad(x)


# an intermediary class that attaches a player to a controller and maps keys on that controller
class interface():
    def __init__(self, controller):
        self.controller = controller

        # essentially, this class is a button to action translation device. It has several internal vars that pass
        # themselves into the attached controller as lookups to determine if the button has been pressed
        self.primary_fire = 'X'
        self.secondary_fire = 'Y'
        self.back = 'B'
        self.accept = 'A'
        self.r_spell = 'RB'
        self.l_spell = 'LB'

        # the moving field is important because the player class references it to determine if and how fast the player
        # should be moving
        self.moving = (0, 0)
        self.direction = (0, 0)

    def update(self):
        self.controller.update()
        mov_x = float(self.controller.left_stick['X'])
        mov_y = float(self.controller.left_stick['Y'])
        self.moving = (mov_x, mov_y)
        dir_x, dir_y = 0, 0
        if (self.controller.right_stick['X']) > deadzone:
            dir_x = 1
        elif (self.controller.right_stick['X']) < -(deadzone):
            dir_x = -1

        if (self.controller.right_stick['Y']) > deadzone:
            dir_y = 1
        elif (self.controller.right_stick['Y']) < -(deadzone):
            dir_y = -1

        self.direction = (dir_x, dir_y)


    # checks if the fire key was pressed this frame or the previous frame
    def check_fire(self):
        return self.controller.pull_button(self.primary_fire)

    def next_spell(self):
        then, now = self.controller.pull_button(self.r_spell)
        if now and not then:
            return True
        else:
            return False

    def prev_spell(self):
        then, now = self.controller.pull_button(self.l_spell)
        if now and not then:
            return True
        else:
            return False


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
        print(jub.get_name())

        self.left_stick = {'X': jub.get_axis(0), 'Y': jub.get_axis(1)}
        self.right_stick = {'X': jub.get_axis(3), 'Y': jub.get_axis(4)}
        self.triggers = {'RT': jub.get_axis(2)}
        self.buttons = {'A': jub.get_button(0), 'B': jub.get_button(1),
                        'X': jub.get_button(2), 'Y': jub.get_button(3),
                        'LB': jub.get_button(4), 'RB': jub.get_button(5),
                        'Start': jub.get_button(7), 'Select': jub.get_button(6),
                        'LStick': jub.get_button(8), 'RStick': jub.get_button(9)}

        self.new_left_stick = {'X': jub.get_axis(0), 'Y': jub.get_axis(1)}
        self.new_right_stick = {'X': jub.get_axis(3), 'Y': jub.get_axis(4)}
        self.new_triggers = {'RT': jub.get_axis(2)}
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
        self.right_stick = self.new_right_stick
        self.left_stick = self.new_left_stick
        self.triggers = self.new_triggers

        self.new_buttons = {
                               'A': self.jub.get_button(0), 'B': self.jub.get_button(1),
                               'X': self.jub.get_button(2), 'Y': self.jub.get_button(3),
                               'LB': self.jub.get_button(4), 'RB': self.jub.get_button(5),
                               'Start': self.jub.get_button(7), 'Select': self.jub.get_button(6),
                               'LStick': self.jub.get_button(8), 'RStick': self.jub.get_button(9)
                            }
        self.new_left_stick = {'X': self.jub.get_axis(0), 'Y': self.jub.get_axis(1)}
        self.new_right_stick = {'X': self.jub.get_axis(4), 'Y': self.jub.get_axis(3)}

        # the triggers are special, in that they are not 2 separate axes, but instead the signed difference between
        #  both triggers as a single axis. If RT is pressed, axis 2 is
        self.new_triggers = {'Triggers': self.jub.get_axis(2)}

    # returns the old and new input states for a single button (this allows button mapping at the player level)
    def pull_button(self, button_name):
        return self.buttons[button_name], self.new_buttons[button_name]

    def pull_left_stick(self):
        return self.left_stick, self.new_left_stick

    def pull_right_stick(self):
        return self.right_stick, self.new_right_stick


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
        print(jub.get_name())

        self.left_stick = {'X': jub.get_axis(0), 'Y': jub.get_axis(1)}
        self.right_stick = {'X': jub.get_axis(3), 'Y': jub.get_axis(4)}
        self.triggers = {'Triggers': jub.get_axis(2)}
        self.buttons = {'A': jub.get_button(0), 'B': jub.get_button(1),
                        'X': jub.get_button(2), 'Y': jub.get_button(3),
                        'LB': jub.get_button(4), 'RB': jub.get_button(5),
                        'Start': jub.get_button(7), 'Select': jub.get_button(6),
                        'LStick': jub.get_button(8), 'RStick': jub.get_button(9)}

        self.new_left_stick = {'X': jub.get_axis(0), 'Y': jub.get_axis(1)}
        self.new_right_stick = {'X': jub.get_axis(3), 'Y': jub.get_axis(4)}
        self.new_triggers = {'Triggers': jub.get_axis(2)}
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
        jub = self.jub

        self.buttons = self.new_buttons
        self.right_stick = self.new_right_stick
        self.left_stick = self.new_left_stick
        self.triggers = self.new_triggers

        self.new_buttons = {
                               'A': jub.get_button(0), 'B': jub.get_button(1),
                               'X': jub.get_button(2), 'Y': jub.get_button(3),
                               'LB': jub.get_button(4), 'RB': jub.get_button(5),
                               'Start': jub.get_button(7), 'Select': jub.get_button(6),
                               'LStick': jub.get_button(8), 'RStick': jub.get_button(9)
                            }
        self.new_left_stick = {'X': jub.get_axis(0), 'Y': jub.get_axis(1)}
        self.new_right_stick = {'X': jub.get_axis(4), 'Y': jub.get_axis(3)}

        # the triggers are special, in that they are not 2 separate axes, but instead the signed difference between
        #  both triggers as a single axis
        self.new_triggers = {'Triggers': jub.get_axis(2)}


    # the following pull methods return the old and new input states for the given buttin/axis/stick
    # (this allows button mapping at the player level)
    # a single button
    def pull_button(self, button_name):
        return self.buttons[button_name], self.new_buttons[button_name]

    # the left stick
    def pull_left_stick(self):
        return self.left_stick, self.new_left_stick

    # the right stick
    def pull_right_stick(self):
        return self.right_stick, self.new_right_stick


# super basice keyboard class for keyboard input. like the controllers, it stores two frames of input
class keyboard():
    def __init__(self):
        self.key = pygame.key.get_pressed()
        self.new_key = pygame.key.get_pressed()

    def update(self):
        self.key = self.new_key
        self.new_key = pygame.key.get_pressed()