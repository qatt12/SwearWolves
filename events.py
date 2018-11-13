import pygame, sys


# events will be expanded to cover printing stuff to the log files under a variety of conditions
base = pygame.USEREVENT
game_state = base + 10
enter_start = game_state + 1
exit_start = game_state + 2
enter_char_select = game_state + 3
exit_char_select = game_state + 4
enter_game = game_state + 5
exit_game = game_state + 6



door = base + 20

class event_handler():
    def __init__(self, tracking_level):
        self.error_log = open("error.txt", 'w')
        self.log = open("log.txt", 'w')
        self.trace_log = open('trace.txt', 'w')
        self.tracking_level = tracking_level

        self.console_buffer = []
        self.log_buffer = []

    def generic_event(self, num, name, force_to_console=False, force_to_log=False, track_log=sys.__stdout__, *args, **kwargs):
        ret = pygame.event.Event(num)
        msg = str(num, name)

        if force_to_console:
            print(msg, args)

        if force_to_log:
            print(msg, args, file=track_log)

        if 'console_msg' in kwargs:
            print(num, name, kwargs['console_msg'])

        if 'log_entry' in kwargs:
            print(num, name, kwargs['log_entry'], file=track_log)

        pygame.event.post(ret)

    def game_state_event(self, sub_num):
        ret = pygame.event.Event(game_state + sub_num)
        pygame.event.post(ret)

    def begin_start(self):
        self.game_state_event(enter_start)

    def end_start(self):
        self.game_state_event(exit_start)

    def begin_char_select(self):
        self.game_state_event(enter_char_select)

    def end_char_select(self):
        self.game_state_event(exit_char_select)

    def begin_main_game(self):
        self.game_state_event(enter_game)

    def end_main_game(self):
        self.game_state_event(exit_game)

    def minor_event(self, file_src, class_src, instance_src):
        pass

    def build_log(self, file_id, name, **kwargs):
        ret = ""
        ret += file_id, "| ", name, "\n\t"
        for key in kwargs:
            ret += key, ": ", kwargs[key], "\n\t"
        return ret

    def to_console(self, *args, **kwargs):
        print(self.build_log(*args, **kwargs))

import pygame

x = 0
next_stage = 1

def new_event(num, name, print_self=False, **kwargs):
    ret = pygame.event.Event(pygame.USEREVENT+num, message="STUFF")
    if "console_msg" in kwargs:
        print(kwargs['console_msg'])
    if print_self:
        print("Name: ", name, " User#: ", num, "Pygame#:", pygame.USEREVENT+num)
    pygame.event.post(ret)
    return "NULL"