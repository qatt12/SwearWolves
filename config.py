# configuration options
# contains the important config/initialization params in a central location.

fps = 128
screen_size = (1300, 700)
screen_width = screen_size[0]
screen_height = screen_size[1]
field_size = (1200, 600)

# constants for the proportional size of the players' HUDs
hud_width_proportion = 3
hud_height_proportion = 5

# size of the tiles used to draw floors and such
tile_scalar = 100

# colors
green  =    (  0, 255,   0)
red    =    (255,   0,   0)
blue   =    (  0,   0, 255)
white  =    (255, 255, 255)
black  =    (  0,   0,   0)
purple =    (200,   0, 200)
yellow =    (200, 200,   0)

default_transparency = (255, 174, 201)

# color, but in a dictionary
color_lookup = {
    'green'  :    (  0, 255,   0),
    'red'    :    (255,   0,   0),
    'blue'   :    (  0,   0, 255),
    'white'  :    (  0,   0,   0),
    'black'  :    (255, 255, 255),
    'green2' :    ( 30, 255,  60),
    'red2'   :    (255,  30,  60),
    'blue2'  :    ( 30,  60, 255),
    'idk'    :    (255, 255,   0),
    1        :    ( 30, 255,  60),
    2        :    (255,  30,  60),
    3        :    ( 30,  60, 255),
    4        :    (255, 255,   0)
}

###
# part of my attempts to convert this whole thing to a layeredUpdates instead of fifty sprite groups. Doesn't make sense
# to try and do that while so much is still unfinished tho
# think of these as layer constants, used to organize everything into the proper hierarchy of draw order
# note that there are several blank layers in between the major divisions/categories. This is to give us some wiggle
# room for stuff that has to be drawn in a particular way
bottom_layer = 0                      # this layer is basically unseen, usable as a background
floor_layer = 1                       # 1
floor_cos = floor_layer + 1           # 2
                                      # 3
outer_wall_layer = floor_cos + 2      # 4
inner_wall_layer = outer_wall_layer+1 # 5
door_layer = inner_wall_layer+1       # 6
wall_cos = door_layer+1               # 7
                                      # 8
player_layer = floor_cos+7            # 9
                                      # 10
                                      # 11
                                      # 12
enemy_layer = player_layer+4          # 13
                                      # 14
                                      # 15
                                      # 16
spell_layer = enemy_layer+1           # 17

spark_layer = spell_layer +4          # 18
missile_layer = spark_layer+1         # 19
impact_layer = missile_layer+1        # 20
air_layer = missile_layer + 4         # 21
                                      # 22
                                      # 23
                                      # 24
overlayer = air_layer + 4             # 25
menu_layer = overlayer+1              # 26
button_layer = menu_layer+1           # 27