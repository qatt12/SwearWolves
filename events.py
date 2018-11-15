import pygame, collections

base = pygame.USEREVENT
game_state_event = base
room_event = base +1
player_event = base +2
file_event = base +3
buffer_flush_event = base +4


# event_handler has two purposes: handling events (duh), and handling entries.
# four types of entry exist (error, event, log, and trace), three are commonly used (error, log, trace), and two are
# (debatebly) good things (trace, log)
# naming conventions: I've tried to be as consistent as possible with this; let me explain it all here:
# 1) at the top of every file, right after the file waifu, events.py is imported. right after this, event_maker is
# imported (i used "from events import event_maker" so that event_maker would appear exactly the same every time it was
# invoked; you can directly call event_maker from any file)
# 2) I included several dummy "if [BLANK] in kwargs:" statements as part of the various methods involving entries to
# remind us what the special kwargs are
# 3) you motherfuckers better not throw random print statements every to debug shit, MAKE OR SEND AN ENTRY
# 4) I'm sorry, I didn't mean to get hostile, you're all great. As long as you use the entry system
# 5) event_maker is the name of a (indeed the ONLY) specific instance of the event_handler class. It is imported to
# every file, and across every file, it is the same instance
# 6) to describe standard syntax conventions, I use ///[(FILE.)CONTENT(.BLAH)]/// broken down, this is:
#       I use a leading three slashes and a trailing three slashes when I need to avoid using "quotes", this is because
#       using "quotes" implies that you are supposed to send a string. this form: ///OBJECT///
#
#       I use all caps to denote that a (non-specific) file, class, or method name needs to be substituted into that
#       location. This is different from a specific method or instance (not class). If I name a particular class, then
#       it should be the class name of that class OR ONE OF ITS CHILDREN. Ex: CLASS can be any class of object
#       (int, spriteling, etc) but NOT a particular instance of such objects. FILE can be any .py file. METHOD can be
#       any method of the specified class (assuming its of the form: CLASS.METHOD ). If its in lowercase, I'm looking
#       for an exact instance or the specific method enumerated
#
#       I use [brackets] to describe a single, contiguous, self-contained param/entry (entry here IS NOT referring to
#       the entry class defined in this, or any other, file). this sets it apart from any other data of a different
#       type/format that is to be entered alongside it
#
#       Finally, I use (parentheses) within [brackets] to denote an optional param/extension
#
#       Side Note: blah is my go-to for any generic/vague/non-specific substitution of data
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

        # log_permissions determines which types of entry will be printed to the log upon being sent. If it doesn't have
        # permission here, then it will only end up on the buffer, which must be flushed to the log. Note that every
        # type of entry is assumed to have buffer permission (thus, every successfully sent entry will be placed into
        # the buffer, of those, some will print to the log, and not exclusive with this group, some will print to
        # console. This is overridden by the force_to_log param in send/make entry
        self.log_permissions = {
            'trace': False,
            'log':   True,
            'event': False,
            'error': True
        }

        # this is where you can set the policy for what is automagically sent to the console. Useful if you're Debugging
        # a particular file or set of features with the same terms, and you want to print them directly to console
        # (without having to force them to console, which must be manually don/undone).
        self.terms_to_console = []
        self.files_to_console = []

        # simple maps that (re)direct the incoming entries to the proper logs and/or buffers
        self.buffer_sort= {
            'trace': self.trace_buffer,
            'log':   self.log_buffer  ,
            'event': self.event_buffer
        }

        self.entry_sort = {
            'trace': self.trace_log,
            'log':   self.log      ,
            'event': self.event_log,
            'error': self.error_log
            }

    # make_entry lets you create and send an entry with the same function. used in the majority of cases, as you will
    # generally want to make and send an entry at the same time. you need to fill in all the same info as you would need
    # to construct an entry, plus two extra fields: force_to_console and force_to_log. If either or both of these are
    # true, it force-prints the entry to the console or log, res. Keep in mind that these DO NOT bypass the
    # event_maker's policies for blocked files or terms: if an entry comes from a blocked file, or carries a blocked
    # term, it will not make it to the buffer OR the log OR even to the console.
    # make_entry is barely different from send_entry, in that it also constructs the entry for you, before calling
    # send_entry
    # note that both return a boolean value representing whether or not the entry you tried to send actually made it to
    # the buffer or log
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

        # Look at that, its screening out entries that come from blocked files
        if fil_src not in self.blocked_files:
            ret = entry(type, name, desc, fil_src, *args, **kwargs)
            return self.send_entry(ret, force_to_console, force_to_log)

    # dispatches an entry into the event_handler, passing it thru a series of logic gates and directional maps to decide
    # where it ultimately ends up
    def send_entry(self, message, force_to_console=True, force_to_log=False):
        if message.get_file_source() not in self.blocked_files:
            if message.screen_terms(self.blocked_terms):
                if self.log_permissions[message.get_type()] or force_to_log or message.get_type() == 'error':
                    print(message, file=self.entry_sort[message.get_type()])
                else:
                    self.buffer_sort[message.get_type()].append(message)
                if force_to_console or message.match_terms(self.terms_to_console) or message.get_file_source() in self.files_to_console:
                    print(message)
                return True
        return False

    # posts an event. basically an expansion on the standard pygame event that automagically generates a valid entry to
    # accompany the event (unless you provide one yourself, using the 'entry' kwarg)
    def new_event(self, event_num, file_src='events', *args, **kwargs):
        ret = pygame.event.Event(event_num, **kwargs)
        pygame.event.post(ret)
        if 'entry' in kwargs:
            self.send_entry(kwargs['entry'])
        else:
            self.make_entry('event', str(event_num), str(ret), file_src, False, False, *args, **kwargs)

    # adjusts which terms and files get sent to console
    def add_console_permissions(self, **kwargs):
        if "terms" in kwargs:
            for each in kwargs['terms']:
                self.terms_to_console.append(each)
        if 'files' in kwargs:
            for each in kwargs['files']:
                self.files_to_console.append(each)

    # flushes the trace buffer to the trace log, optionally also to console and optionally emptying out all its contents
    # all of the params are optional, so you can just call this and tell it to dump the contents of the trace buffer
    # both to console and to the trace log, emptying out the buffer as you go. BUUUUUUUUUT......
    # you may instead provide a flush message, to be printed at the top of the log, just below the line of stars used
    # to delineate this from other entries, you can then decide if you want to also print the contents of the buffer to
    # the console by defining the value of the aptly named to_console, that in turn, finally allows you to decide if you
    # also want to empty the buffer out as you go
    # beyond those default params, you can use the kwargs['block_terms'] to block all entries with certain terms,
    # kwargs['allow_terms'] to only allow entries that contain certain terms
    # provide a custom screening method that returns true to let the entry pass, or false to stop it
    # you may also want to specify the number of entries you want printed w/ kwargs['num_entries'], this currently does
    # nothing, but good on you for knowing what you want and not being afraid to go for it
    # finally, you can specify an additional destination log for the trace buffer, (this must be the string name of one
    # of the other logs) to which the remaining entries (as determined by the provided filter(s)) will ALSO be printed
    # IN ADDITION TO the trace log
    def flush_trace_buffer(self, flush_message="FLUSH", to_console=True, empty=True, **kwargs):
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

        if empty:
            while len(self.trace_buffer) > 0:
                temp = ret.pop()
                if to_console:
                    print(temp)
                print(temp, file=self.trace_log)
                if 'dest' in kwargs:
                    print(temp, file=self.entry_sort[kwargs['dest']])
        else:
            for each in ret:
                if to_console:
                    print(each)
                print(each, file=self.trace_log)
                if 'dest' in kwargs:
                    print(each, file=self.entry_sort[kwargs['dest']])

        print("**********************************************************************************", file=self.trace_log)


# a data storage/organization class for recording and formatting whatever info you give it. designed to track the
# sequential numbering of the entry, the file from which it was sent, the name of the entry, a short description of its
# contents, and then a list of terms (that can be used to block or permit the entry from going to console or log), plus
# a set of key-word args, some of which are defined and have a specific purpose, others are just printed
# the type must be either 'error', 'event', 'trace', or 'log', otherwise bad things happen.
# for some entries, having both a name and a description is redundant; in those cases, leave desc blank "".
class entry():
    num = 0
    def __init__(self, type, name, desc, file_src, *args, **kwargs):
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
        # these do serve as an opportunity for me to explain the special kwargs; the entry constructor will take and
        # save whatever kwargs you send it, so you can send it whatever (valid params) you want. BUUUUUUT....
        # I have defined several special kwargs that appear in specific locations when the entry is turned into a string
        # they are listed below
        # obj_src : the class name from which the entry is sent. syntactically: ///FILE.CLASS///, where CLASS is the
        # class name of the calling object. CLASS can also be substituted for a method (if the method is standalone
        # within FILE) or appended onto the CLASS (but usually its preferable to informally describe the method of
        # origin in the loc_src kwarg instead)
        # loc_src : an informal "string" description of where the entry came from.
        # inst_src : the particular instance (of an object/class) from which this entry originated. Always do this as
        # ///inst_src=self///
        # log_entry : Supposed to keep a running log of the entry/subject that changes over time. Beyond that, its just
        # a special kwarg that pretty much just appears at the top of the entry when converted to string. Put whatever
        # you want (to be at the top of the printed entry) into here.
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
        self.file_src = file_src
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
            terms += "\n\tterms: "
            for each in self.terms:
                terms += each
                terms += "; "

        k_wargs = ""
        if len(self.k_v) > 0:
            k_wargs += "\n\tkey words:\n\t"
            for key in self.k_v:
                k_wargs += str(key)
                k_wargs += ": "
                if self.k_v[key] is not None:
                    k_wargs += str(self.k_v[key])
                k_wargs += "\n\t"

        return header + "\n" + content +  terms + k_wargs

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
            if key == 'remove_key':
                self.k_v[key] = None
            elif key == 'remove_term':
                self.terms = [t for t in self.terms if t not in kwargs['remove_term']]
            elif key == 'add_term':
                for each in kwargs['add_term']:
                    self.terms.append(each)
            elif key == 'new_desc':
                self.desc = kwargs['new_desc']
            elif key == 'ext_desc':
                self.desc += kwargs['ext_desc']
            elif key == 'log_entry':
                if 'log_entry' in self.k_v:
                    self.k_v['log_entry'] += kwargs['log_entry']
                else:
                    self.k_v['log_entry'] = kwargs['log_entry']
            else:
                self.k_v[key] = kwargs[key]
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
event_maker.add_console_permissions(terms=['Logan'])
event_maker.make_entry("trace", "first trace", 'the very first trace entry', 'events', False, False)