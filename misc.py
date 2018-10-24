import pygame, controllers
from interface import handler as handler

# manages currently active controllers, available controllers, and adding new controllers/players to the game
class controller_list():
    def __init__(self):
        pygame.joystick.init()
        self.player_num = 0
        self.used_joysticks = []
        self.active_controllers = []
        self.standby_controllers = []
        self.keyboard = controllers.keyboard()
        self.is_keyboard = False

    def update(self):
        pygame.joystick.init()
        possible_controllers = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        #print("possible: ", possible_controllers)
        standby_controllers = [controllers.auto_assign(each) for each in possible_controllers]

        #print("standby: ", standby_controllers)
        #print("keyboard: ", self.is_keyboard)
        for each in standby_controllers:
            # print("each standby controller: ", each)
            each.update()
            if each.check_status() and each.jub.get_id() not in self.used_joysticks:
                self.active_controllers.append(each)
                self.used_joysticks.append(each.jub.get_id())
        self.keyboard.update()
        if self.keyboard.check_status() and self.is_keyboard is False:
            self.is_keyboard = True
            self.active_controllers.append(self.keyboard)

    def is_p1_ready(self):
        #print("is p1 ready")
        if len(self.active_controllers) > 0:
            self.player_num += 1
            # print("ticking player num from p1")
            return True
        else:
            return False

    def get_p1(self):
        # print("getting p1")
        if self.active_controllers[0]:
            return handler(self.active_controllers[0], console_message="got player one")

    def get_next_player(self):
        # print("getting next")
        # print("ticking player num from next")
        self.player_num += 1
        return handler(self.active_controllers[self.player_num-1], console_message="got next player")

    def is_next_ready(self):
        # print("is next ready")
        # print("active controllers: ", self.active_controllers)
        # print("active joysticks: ", self.used_joysticks, "misc player num= ", self.player_num, "active controller num= ", len(self.active_controllers))
        if len(self.active_controllers) > self.player_num:
            return True
        return False


class player_list():
    def __init__(self, p1):
        self.player_one = p1
        self.player_two = None
        self.player_three = None
        self.player_four = None

    def add_next_player(self, next_player):
        if self.player_two is None:
            self.player_two = next_player
        elif self.player_three is None:
            self.player_three = next_player
        elif self.player_four is None:
            self.player_four = next_player

    def update(self, *args, **kwargs):
        self.player_one.update(*args, **kwargs)
        self.player_two.update(*args, **kwargs)
        self.player_three.update(*args, **kwargs)
        self.player_four.update(*args, **kwargs)