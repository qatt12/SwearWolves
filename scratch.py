
import timeit

print(
    timeit.timeit('r0 = r0.move(52, 88)',
'''import pygame
pygame.init() 
r0 = pygame.rect.Rect((0, 0), (10, 10))'''
              )
)

print(
    timeit.timeit('r1.move_ip(52, 88)',
'''import pygame
pygame.init()
r1 = pygame.rect.Rect((0, 0), (10, 10))'''
              )
)
