import libtcodpy as libtcod
from MapBuilder import *
from Config import rng

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Test RL', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

builder = LevelBuilder()

area = builder.buildArea(5, 5)

print area[1][2].tiles[4][5].glyph

ranPoint = area[1][1].free_random_location()

aMap = area[1][1]

print ranPoint.getPos()

libtcod.line_init(2,2,5,8)


#### START OF PATHTEST
####
fov_map = libtcod.map_new(aMap.width,aMap.height)
for y in range(aMap.height):
        for x in range(aMap.width):
            tcod.map_set_properties(fov_map, x, y, not aMap.tiles[x][y].block_sight, aMap.tiles[x][y].movecost > 0)

libtcod.map_compute_fov(fov_map, 6, 7, 40, True, 0)


path = libtcod.path_new_using_map(fov_map,  1.0)



start = aMap.free_random_location()
end = aMap.free_random_location()

print libtcod.map_is_walkable(fov_map,start.x,start.y)
print start.x,start.y,end.x,end.y

libtcod.path_compute(path,start.x,start.y,end.x,end.y)

print libtcod.path_get_origin(path)
print libtcod.path_get_destination(path)

print libtcod.path_size(path)

print libtcod.path_is_empty(path)

print libtcod.path_walk(path, True)
print libtcod.path_size(path)
print libtcod.path_walk(path, True)
print libtcod.path_size(path)

#print libtcod.path_get(path,4)
###
### END OF PATHTEST

"""
state = True
while state:
    print "1"
    key = libtcod.console_wait_for_keypress(True)

    if libtcod.console_is_key_pressed(libtcod.KEY_UP) or libtcod.console_is_key_pressed(libtcod.KEY_KP8):
                print "Pressed UP"

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or libtcod.console_is_key_pressed(libtcod.KEY_KP2):
                print "Pressed DOWN"

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or libtcod.console_is_key_pressed(libtcod.KEY_KP4):
                print "Pressed LEFT"

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or libtcod.console_is_key_pressed(libtcod.KEY_KP6):
                print "Pressed RIGHT"

    elif libtcod.console_is_key_pressed(libtcod.KEY_ESCAPE):
                print "ESCPAE"
                state = False


"""