import pygame, sys

base = pygame.USEREVENT
game_state_event = base
room_event = base +1


class event_handler():
    def __init__(self, **kwargs):
        self.error_log = open("error.txt", 'w')
        self.log = open("log.txt", 'w')
        self.trace_log = open('trace.txt', 'w')
        self.event_log = open("event_log.txt", 'w')

        self.blocked_files = []
        self.blocked_terms = []
        self.term_bypass = []

        self.log_buffer = []
        self.trace_buffer = []
        self.event_buffer = []

        self.log_permissions = {
            'trace': True,
            'log':   True,
            'event': True,
            'error': True
        }

        self.terms_to_console = []
        self.files_to_console = []

        self.buffer_sort= {
            'trace': self.trace_buffer,
            'log':   self.log_buffer  ,
            'event': self.event_buffer,
        }

        self.entry_sort = {
            'trace': self.trace_log,
            'log':   self.log      ,
            'event': self.event_log,
            'error': self.error_log
            }

    def make_entry(self, type, name, desc, fil_src, force_to_console=True, force_to_log=False, *args, **kwargs):
        if fil_src not in self.blocked_files:
            ret = entry(type, name, desc, fil_src, *args, **kwargs)
            return self.send_entry(ret, force_to_console, force_to_log)

    def send_entry(self, message, force_to_console=True, force_to_log=False):
        if message.get_file_source() not in self.blocked_files:
            if not message.screen_terms(self.blocked_terms):
                if self.log_permissions[message.get_type()] or force_to_log:
                    print(message, file=self.entry_sort[message.get_type()])
                else:
                    self.buffer_sort[message.get_type()].append(message)
                if force_to_console or message.match_terms(self.terms_to_console) or message.get_file_source() in self.files_to_console:
                    print(message)
                return True
        return False

    def new_event(self, event_num, **kwargs):
        pygame.event.post(pygame.event.Event(event_num, **kwargs))
        if 'entry' in kwargs:
            self.send_entry(kwargs['entry'])

    def add_console_permissions(self, **kwargs):
        if "terms" in kwargs:
            for each in kwargs['terms']:
                self.terms_to_console.append(each)
        if 'files' in kwargs:
            for each in kwargs['files']:
                self.terms_to_console.append(each)

class entry():
    num = 0
    def __init__(self, type, name, desc, fil_src, *args, **kwargs):
        entry.tick_tracker()
        self.entry_num = entry.get_tracker()
        try:
            assert (type == 'trace' or type == 'log' or type == 'event' or type == 'error'), "improper entry type"
        except AssertionError:
            print(AssertionError, "need: event, error, trace, or log; found: ", type)
            self.type = 'type error'
        else:
            self.type = type

        self.terms = []
        for each in args:
            self.terms.append(each)
        self.name = name
        self.desc = desc
        self.file_src = fil_src
        self.k_v = kwargs

    def __str__(self):
        header = "***\tentry #: " + str(self.entry_num) + " type: " + self.type + '\n' + "file source: " + str(self.file_src)
        if 'obj_src' in self.k_v:
            header = header + "| obj source: " + str(self.k_v['obj_src'])
        if 'inst_src' in self.k_v:
            header = header + "| instance source: " + str(self.k_v['inst_src'])
        if 'loc_src' in self.k_v:
            header = header + "| loc source: " + self.k_v['loc_src']
        content = self.name + ": " + self.desc
        if 'log_entry' in self.k_v:
            content = content + "; " + str(self.k_v['log_entry'])

        terms = ""
        if len(self.terms) > 0:
            terms += "\tterms: "
            for each in self.terms:
                terms += each
                terms += "; "

        k_wargs = ""
        if len(self.k_v) > 0:
            k_wargs += "\tkey words:\n\t"
            for key in self.k_v:
                k_wargs += str(key)
                k_wargs += ": "
                k_wargs += str(self.k_v[key])
                k_wargs += "\n\t"

        return header + "\n" + content + '\n' + terms + '\n' + k_wargs

    def get_type(self):
        return self.type

    def get_file_source(self):
        return self.file_src

    def screen_terms(self, blocked, **kwargs):
        if "bypass" in kwargs:
            for each in kwargs['bypass']:
                if any in self.terms == each:
                    return True
        if any in self.terms in blocked:
            return False

    def match_terms(self, allowed):
        for each in self.terms:
            if each in allowed:
                return True
        else:
            return False

    @classmethod
    def tick_tracker(cls):
        cls.num += 1

    @classmethod
    def get_tracker(cls):
        return cls.num

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

event_maker = event_handler()
event_maker.add_console_permissions(terms=['theme', 'user'])