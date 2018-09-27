import pygame, controllers
from interface import handler as handler

class controller_list():
    def __init__(self):
        self.active_controllers = []
        self.standby_controllers = []

    def update(self):
        possible_controllers = controllers.prepare_joysticks()
        print("possible: ", self.standby_controllers)
        standby_controllers = [controllers.auto_assign(each) for each in possible_controllers]

        print("standby: ", standby_controllers)
        for each in standby_controllers:
            each.update()
            if each.check_status():
                self.active_controllers.append(each)
        keyboard = controllers.keyboard()
        if keyboard.check_status():
            self.active_controllers.append(keyboard)

    def is_p1_ready(self):
        print("is p1 ready")
        if len(self.active_controllers) > 0:
            return True
        else:
            return False

    def get_p1(self):
        print("getting p1")
        if self.active_controllers[0]:
            return handler(self.active_controllers[0])
