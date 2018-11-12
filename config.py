#configuration options
#contains the important config/initialization params in a central location.

fps = 128
screen_size = (1200, 700)
screen_width = screen_size[0]
screen_height = screen_size[1]
field_size = (1400, 700)

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

# color, but in a dicrioanry
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
