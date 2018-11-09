import pygame, sys

# events will be expanded to cover printing stuff to the log files under a variety of conditions

x = 0
next_stage = pygame.USEREVENT+1




def new_event(num, name, print_self=False, track_log=sys.__stdout__, **kwargs):
    ret = pygame.event.Event(pygame.USEREVENT+num, message="STUFF")
    print("track_log: ", track_log)
    if "console_msg" in kwargs:
        print(kwargs['console_msg'])

    if print_self and 'log_entry' in kwargs:
        print("Name: ", name, " User#: ", num, "Pygame#:", pygame.USEREVENT + num, ":: ", kwargs['log_entry'],
              file=track_log)
    elif print_self:
        print("Name: ", name, " User#: ", num, "Pygame#:", pygame.USEREVENT+num, file=track_log)

    pygame.event.post(ret)
    return "NULL"

