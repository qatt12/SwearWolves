import pygame


# loads all the necessary images/surfaces. may be replaced with a single centralized python file that just loads up
# images and is imported into other files
missile_sheet = pygame.image.load('projectiles\simple_missiles.png').convert_alpha()

fire_bolt_img = missile_sheet.subsurface((1, 1), (66, 66))
acid_bolt_img = missile_sheet.subsurface((68, 1), (66, 66))
frost_bolt_img = missile_sheet.subsurface((135, 1), (66, 66))


lava_balls = missile_sheet.subsurface((1, 135), (66, 66))
lava_ball = missile_sheet.subsurface((1, 202), (66, 66))

snow_balls = missile_sheet.subsurface((135, 135), (66, 66))
snow_ball = missile_sheet.subsurface((135, 202), (66, 66))

acid_balls = missile_sheet.subsurface((68, 135), (66, 66))
acid_ball = missile_sheet.subsurface((68, 202), (66, 66))

tri_bolt = missile_sheet.subsurface((202, 1), (66, 66))
quad_bolt = missile_sheet.subsurface((202, 68), (66, 66))
penta_bolt = missile_sheet.subsurface((202, 135), (66, 66))
hex_bolt = missile_sheet.subsurface((202, 202), (66, 66))

idle_flame = missile_sheet.subsurface((2, 69), (64, 36))
idle_cloud = missile_sheet.subsurface((79, 73), (43, 46))
snow_flakes = missile_sheet.subsurface((164, 103), (29, 15))


#BEAMS/RAYS
all_rays = pygame.image.load('projectiles\simple_rays.png').convert_alpha()
hot_rays = all_rays.subsurface((0, 0), (56, 18))
cold_rays = all_rays.subsurface((0, 19), (56, 18))
acid_rays = all_rays.subsurface((0, 38), (56, 18))
hot_ray_1 = hot_rays.subsurface((0, 0), (18, 18))
cold_ray_1 = cold_rays.subsurface((0, 0), (18, 18))