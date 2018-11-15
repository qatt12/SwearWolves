import pygame, collections

base = pygame.USEREVENT
game_state_event = base
room_event = base +1
player_event = base +2
file_event = base +3
buffer_flush_event = base +4


# event_handler has two purposes: handling events (duh), and handling entries.
# four types of entry exist (erro, event, log, and trace), three are commonly used (error, log, trace), and two are good
# things (trace, log)
# technically, the difference between them is minimal, aside from the default settings. By default:
#
# event entries are only made alongside a user-defined event, either automatically or as provided. They are held in the
# buffer unless (also) forced to log (event_log.txt)
#
# error entries SHOULD be made whenever an error arises, this means that we should have AT LEAST one error entry per
# try/except statement, possibly more. Error entries are usually printed to log (error.txt), but may crash the game
# before that happens (potentially before they even get made). Ideally, they should have some suggestions, possibly even
# some recovery code for fixing them
#
# trace entries are the most common, make them basically whenever you want to track something going on in the
# environment, either for context or... whatever else i guess? Trace entries should be your go-to. these are not printed
# to log (unless they are forced), instead they are stored in the trace buffer, which holds 50 entries. If it ever
# exceeds that, it will start dumping the oldest entries, one by one, as new entries are added. This trace buffer can be
# flushed to log (trace.txt) with the appropriately named "flush_trace_buffer" method. more on that below
#
# log entries are the second most common. They are printed to log (log.txt) by default. Make these every time a
# unique/one-off "thing" happens, or at least be careful enough to only make log entries infrequently. Avoid making them
# as part of a loop and/or an indefinitely repeating block of code.

# the member data for event_handler is basically a bunch of permissions and maps, dictating what is going where and if
# its allowed to or not
class event_handler():
    def __init__(self, log_size, **kwargs):
        # the log files that entries will be sent to.
        # named after the entry type that will be sent to it.
        self.error_log = open("error.txt", 'w')
        self.log = open("log.txt", 'w')
        self.trace_log = open('trace.txt', 'w')
        self.event_log = open("event_log.txt", 'w')

        # blocked_files/terms are lists of exclusions that forbid entries from the enumerated files/bearing the
        # enumerated terms from being recorded (if an entry is excluded here, it won't even make it to the buffer)
        self.blocked_files = []
        if 'blocked_files' in kwargs:
            for each in kwargs['blocked_files']:
                self.blocked_files.append(each)
        self.blocked_terms = []
        if 'blocked_terms' in kwargs:
            for each in kwargs['blocked_terms']:
                self.blocked_files.append(each)

        self.max_log_size = log_size

        self.log_buffer = collections.deque([], self.max_log_size)
        self.trace_buffer = collections.deque([], self.max_log_size)
        self.event_buffer = collections.deque([], self.max_log_size)

        self.log_permissions = {
            'trace': False,
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
        # dummy var and dummy kwargs to get pycharm to offer to autocomplete stuff for me
        temp = None
        if 'obj_src' in kwargs:
            temp = kwargs['obj_src']
        if 'loc_src' in kwargs:
            temp = kwargs['loc_src']
        if 'inst_src' in kwargs:
            temp = kwargs['inst_src']
        if 'log_entry' in kwargs:
            temp = kwargs['log_entry']

        if fil_src not in self.blocked_files:
            ret = entry(type, name, desc, fil_src, *args, **kwargs)
            return self.send_entry(ret, force_to_console, force_to_log)

    def send_entry(self, message, force_to_console=True, force_to_log=False):
        if message.get_file_source() not in self.blocked_files:
            if message.screen_terms(self.blocked_terms):
                if self.log_permissions[message.get_type()] or force_to_log:
                    print(message, file=self.entry_sort[message.get_type()])
                self.buffer_sort[message.get_type()].append(message)
                if force_to_console or message.match_terms(self.terms_to_console) or message.get_file_source() in self.files_to_console:
                    print(message)
                return True
        return False

    def new_event(self, event_num, file_src='events', *args, **kwargs):
        ret = pygame.event.Event(event_num, **kwargs)
        pygame.event.post(ret)
        if 'entry' in kwargs:
            self.send_entry(kwargs['entry'])
        else:
            self.make_entry('event', str(event_num), str(ret), file_src, False, False, *args, **kwargs)

    def add_console_permissions(self, **kwargs):
        if "terms" in kwargs:
            for each in kwargs['terms']:
                self.terms_to_console.append(each)
        if 'files' in kwargs:
            for each in kwargs['files']:
                self.files_to_console.append(each)

    def flush_trace_buffer(self, flush_message, to_console=False, **kwargs):
        print("**********************************************************************************", file=self.trace_log)
        print(flush_message, file=self.trace_log)
        if to_console:
            print(flush_message)
        ret = self.trace_buffer
        if 'block_terms' in kwargs:
            ret = [every for every in self.trace_buffer if every.screen_terms(kwargs['block_terms'])]
        if 'allow_terms' in kwargs:
            ret = [every for every in self.trace_buffer if every.match_terms(kwargs['allow_terms'])]
        if 'screen_by' in kwargs:
            ret = [each for each in self.trace_buffer if kwargs['screen_by'](each)]
        x = len(ret)
        if 'num_entries' in kwargs:
            x = min(kwargs['num_entries'], len(ret))
        for each in ret:
            if to_console:
                print(each)
            print(each, file=self.trace_log)
        print("**********************************************************************************", file=self.trace_log)


# a data storage/organization class for recording and formatting whatever info you give it. designed to track the
# sequential numbering of the entry, the file from which it was sent, the name of the entry, a short description of its
# contents, and then a list of terms (that can be used to block or permit the entry from going to console or log), plus
# a set of key-word args, some of which are defined and have a specific purpose, others are just printed
class entry():
    num = 0
    def __init__(self, type, name, desc, fil_src, *args, **kwargs):
        entry.tick_tracker()
        self.entry_num = entry.get_tracker()
        try:
            assert (type == 'trace' or type == 'log' or type == 'event' or type == 'error'), "improper entry type"
        except AssertionError:
            print(AssertionError, "need: event, error, trace, or log; found: ", type)
            self.type = 'error'
        else:
            self.type = type
        # dummy var and dummy kwargs to get pycharm to offer to autocomplete stuff for me
        temp = None
        if 'obj_src' in kwargs:
            temp = kwargs['obj_src']
        if 'loc_src' in kwargs:
            temp = kwargs['loc_src']
        if 'inst_src' in kwargs:
            temp = kwargs['inst_src']
        if 'log_entry' in kwargs:
            temp = kwargs['log_entry']

        self.terms = []
        for each in args:
            self.terms.append(each)
        self.name = name
        self.desc = desc
        self.file_src = fil_src
        self.k_v = kwargs

    # converts the entry to a string in proper format, with the most relevant info at the top
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
                if self.k_v[key] is not None:
                    k_wargs += str(self.k_v[key])
                k_wargs += "\n\t"

        return header + "\n" + content + '\n' + terms + '\n' + k_wargs

    def get_type(self):
        return self.type

    def get_file_source(self):
        return self.file_src

    # a simple method(ish) for screening out terms we want to block.
    # DEBUG:LOGAN: may want to consider making this more efficient with dicts, but this may not be all that
    # necessary/helpful, as the list we're working with are so small anyways
    # this checks a single entry against a list of blocked terms. if any of this entry's terms are in the list of
    # blocked terms, then it returns false, otherwise it returns true. Additionally, a list of bypass terms can be
    # passed thru kwargs; if this entry contains any of the bypass terms, it automatically passes (without checking
    # against blocked terms) and returns True.
    # thus, this function takes a list of specifically blocked terms and uses it to approve or deny an entry
    def screen_terms(self, blocked, **kwargs):
        if "bypass" in kwargs:
            for each in kwargs['bypass']:
                if any in self.terms == each:
                    return True
        for every in self.terms:
            if every in blocked:
                return False
        return True

    # the opposite of screening. In order to get past this one, this entry needs to have at least one of the
    # specifically enumerated 'allowed' terms.
    def match_terms(self, allowed):
        for each in self.terms:
            if each in allowed:
                return True
        else:
            return False

    def modify(self, *args, **kwargs):
        # dummy var and dummy kwargs to get pycharm to offer to autocomplete stuff for me
        temp = None
        if 'obj_src' in kwargs:
            temp = kwargs['obj_src']
        if 'loc_src' in kwargs:
            temp = kwargs['loc_src']
        if 'inst_src' in kwargs:
            temp = kwargs['inst_src']
        if 'log_entry' in kwargs:
            temp = kwargs['log_entry']
        for key in kwargs:
            if key != 'remove_key':
                self.k_v[key] = None
            if key != 'remove_term':
                self.terms = [t for t in self.terms if t not in kwargs['remove_term']]
            if key != 'add_term':
                for each in kwargs['add_term']:
                    self.terms.append(each)
        # dummy return for getting pycharm to do a thing
        return temp

    @classmethod
    def tick_tracker(cls):
        cls.num += 1

    @classmethod
    def get_tracker(cls):
        return cls.num

import pygame

x = 0
next_stage = 1

event_maker = event_handler(50)
#event_maker.add_console_permissions(terms=['theme', 'user'])
event_maker.make_entry("trace", "first trace", 'the very first trace entry', 'events', False, False)