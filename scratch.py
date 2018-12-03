def tester_f_1(input):
    print(input)

def tester_f_2(input):
    pass

tester_f_1(input=5)

import pygame

t_group1 = pygame.sprite.Group()

def extra_t():
    pass


num = -3.3

print("leftover: ", num % 1)

import math, random

for x in range(0, 50):
    sign = random.randint(0, 2) % 2 * -1
    print(sign)


t_sprite_1 = pygame.sprite.Sprite()
t_sprite_2 = pygame.sprite.Sprite()
t_sprite_3 = pygame.sprite.Sprite()
t_sprite_4 = pygame.sprite.Sprite()
index_test = pygame.sprite.OrderedUpdates(t_sprite_1,
t_sprite_2,
t_sprite_3)

dupe_group_1 = index_test
dupe_group_2 = index_test.copy()
print("at start: ")
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)

index_test.add(t_sprite_4)
dupe_group_1.add(t_sprite_4)
print('at t0: ')
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)

index_test.remove(t_sprite_2)
print('at t1: ')
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)

dupe_group_1.add(t_sprite_2)
print('at t2: ')
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)

dupe_group_2.add(t_sprite_2)
print('at t3: ')
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)

dupe_group_1.remove(t_sprite_3)
print('at t4: ')
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)

dupe_group_2.remove(t_sprite_1)
print('at t5: ')
print("index_test= ", index_test)
print("test 1= ", dupe_group_1)
print("test 2= ", dupe_group_2)


# import timeit
# print(timeit.timeit(
#     '''
# for x in range(0, 1000000):
#     if x%17==0:
#         y+=1
#     ''',
#     '''
# y=0
#     ''',
#     number=100
#               ))
#
# #####BETTER
# print(timeit.timeit(
#     '''
# for x in range(0, 1000000):
#     y+=1
#     if y>=17:
#         y=0
#         z+=1
#     ''',
#     '''
# y, z=0, 0
#     ''',
#     number=100
#              ))
#
# print(timeit.timeit(
#     '''
# for x in range(0, 1000000):
#     y+=1
#     if y==17:
#         y=0
#         z+=1
#     ''',
#     '''
# y, z=0, 0
#     ''',
#     number=100
#              ))

sin_offsets = [2*math.sin(math.radians(x)) for x in range(0, 360)]
print(sin_offsets)

import timeit

print(timeit.timeit(
    '''
ret = r_set.pop()
#print(ret)
r_set.add(ret)
    ''',
    '''
r_set = {0, 1, 2, 3, 4, 5, 6}
    ''',
    number=100000
             ))
print(timeit.timeit(
    '''
random.randint(0, 7)
    ''',
    '''
import random
    ''',
    number=100000
             ))