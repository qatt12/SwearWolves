import pygame

x = 0
next_stage = pygame.USEREVENT+1

def new_event(num, name, print_self=False, **kwargs):
    ret = pygame.event.Event(pygame.USEREVENT+num, message="STUFF")
    if "console_msg" in kwargs:
        print(kwargs['console_msg'])
    if print_self:
        print("Name: ", name, " User#: ", num, "Pygame#:", pygame.USEREVENT+num)
    pygame.event.post(ret)
    return "NULL"

