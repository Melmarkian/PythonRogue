import libtcodpy as tcod
from MapBuilder import LevelBuilder,ObjectBuilder
from Map import Level
from Player import Player
from Time import Time
import textwrap


# Game constants
#

#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Size of the playscreen
CAMERA_WIDTH = 60
CAMERA_HEIGHT = 48

upperLeftX, upperLeftY = 0,0

# FOV libtcod Stuff
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 20
OUT_OF_VIEW_COLOR = tcod.dark_grey

#size of the map
MAP_WIDTH = 120
MAP_HEIGHT = 120

# Bottom Panel
BAR_WIDTH = 20
PANEL_HEIGHT = 2
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT


MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1


# Movement Keys
mKeys = (tcod.KEY_DOWN, tcod.KEY_UP, tcod.KEY_RIGHT, tcod.KEY_LEFT,
         tcod.KEY_KP1, tcod.KEY_KP2, tcod.KEY_KP3, tcod.KEY_KP4,
         tcod.KEY_KP6, tcod.KEY_KP7, tcod.KEY_KP8, tcod.KEY_KP9)

game_msgs = []

class Game:

    builder = LevelBuilder()
    objectBuilder = ObjectBuilder()
    game_msgs = []


    def new_game(self):

        self.init_console()
        self.region = self.init_map()
        self.fov_map = self.init_fov(self.region)
        self.path_map = tcod.path_new_using_map(self.fov_map)
        self.init_population()
        self.init_objects()
        self.player = Player()
        self.buildScreen()

        self.time = Time()



    def init_console(self):

        tcod.console_set_custom_font('arial12x12.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Engel', False)
        self.con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_panel = tcod.console_new(60,2)
        tcod.console_set_color_control(self.bottom_panel,tcod.red,tcod.black)

        self.right_panel = tcod.console_new(20,50)
        tcod.console_set_color_control(self.right_panel,tcod.red,tcod.black)

    def init_fov(self,region):

        fov_map = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tcod.map_set_properties(fov_map, x, y, not self.region.tiles[x][y].block_sight, self.region.tiles[x][y].movecost > 0)

        return fov_map



    def init_map(self):


        region = self.builder.buildLevel(MAP_WIDTH, MAP_HEIGHT)

        return region


    def init_population(self):

        self.region.population = self.builder.populate(self.region)

    def init_objects(self):

        self.region.objects = self.builder.place_objects(self.region)

    def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
        #render a bar (HP, experience, etc). first calculate the width of the bar
        bar_width = int(float(value) / maximum * total_width)

        #render the background first
        tcod.console_set_background_color(self.bottom_panel, back_color)
        tcod.console_rect(self.bottom_panel, x, y, total_width, 1, False)

        #now render the bar on top
        tcod.console_set_background_color(self.bottom_panel, bar_color)
        if bar_width > 0:
            tcod.console_rect(self.bottom_panel, x, y, bar_width, 1, False)

        tcod.console_set_foreground_color(self.bottom_panel,tcod.white)
        tcod.console_print_center(self.bottom_panel, x + total_width / 2, y, tcod.BKGND_NONE,
                                  name + ": " + str(value) + "/" + str(maximum))


    def message(self,new_msg, color = tcod.white):
        #split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

        for line in new_msg_lines:
            #if the buffer is full, remove the first line to make room for the new one
            if len(self.game_msgs) == MSG_HEIGHT:
                del self.game_msgs[0]

            #add the new line as a tuple, with the text and the color
            self.game_msgs.append( (line, color) )


    def buildScreen(self):



            tcod.map_compute_fov(self.fov_map, self.player.posx, self.player.posy, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
            tcod.console_clear(self.con)

            self.move_camera(self.player.posx, self.player.posy)

            for sY in range(CAMERA_HEIGHT):
                for sX in range(CAMERA_WIDTH):
                    x = sX + upperLeftX
                    y = sY + upperLeftY
                    visible = tcod.map_is_in_fov(self.fov_map, x, y)

                    if not visible:
                        if self.region.tiles[x][y].explored:
                            tcod.console_put_char_ex(self.con, sX, sY, self.region.tiles[x][y].glyph, OUT_OF_VIEW_COLOR, self.region.tiles[x][y].backColor)
                    else:
                        tcod.console_put_char_ex(self.con, sX, sY, self.region.tiles[x][y].glyph, self.region.tiles[x][y].charColor, self.region.tiles[x][y].backColor)
                        self.region.tiles[x][y].explored = True

            for pop in self.region.population:
                self.draw(pop)

            for thing in self.region.objects:
                self.draw(thing)

            self.draw(self.player)




            #tcod.console_set_background_color(self.bottom_panel,tcod.black)
            tcod.console_clear(self.bottom_panel)


            #print the game messages, one line at a time
            y = 1
            for (line, color) in self.game_msgs:
                #tcod.console_set_foreground_color(self.bottom_panel, color)
                tcod.console_print_ex(self.bottom_panel, 0, y,0, tcod.LEFT, line)
                y += 1


            tcod.console_blit(self.bottom_panel, 0, 0, 60, PANEL_HEIGHT, 0, 0, PANEL_Y)

            monsterline = 1
            for monster in self.region.population:

                monster_desc = monster.name + " " + str(monster.posx) + " " + str(monster.posy)
                tcod.console_print_ex(self.right_panel, 0, monsterline, 0, tcod.LEFT, monster_desc)
                monsterline += 1

            tcod.console_print_ex(self.right_panel, 0, 40,0,tcod.LEFT, self.region.tiles[self.player.posx][self.player.posy].desc)
            tcod.console_blit(self.right_panel, 0, 0, 0, 0, 0, 60,0 )


            tcod.console_blit(self.con, 0, 0, CAMERA_WIDTH, CAMERA_HEIGHT, 0, 0, 0)
            tcod.console_flush()

    def move_camera(self,target_x, target_y):
        global upperLeftX,upperLeftY

        #new camera coordinates (top-left corner of the screen relative to the map)
        x = target_x - CAMERA_WIDTH / 2  #coordinates so that the target is at the center of the screen
        y = target_y - CAMERA_HEIGHT / 2

        #make sure the camera doesn't see outside the map
        if x < 0: x = 0
        if y < 0: y = 0
        if x > MAP_WIDTH - CAMERA_WIDTH - 1: x = MAP_WIDTH - CAMERA_WIDTH - 1
        if y > MAP_HEIGHT - CAMERA_HEIGHT - 1: y = MAP_HEIGHT - CAMERA_HEIGHT - 1

        #if x != camera_x or y != camera_y: fov_recompute = True

        (upperLeftX, upperLeftY) = (x, y)


    def do_turn(self):


        self.time.increment()
        while self.player.action_points > 0:
            self.get_input2()
            #get_direction
            self.buildScreen()
            #print self.player.action_points
        self.population_move()
        self.timemessage = "Day:" + str(self.time.days)+ ":"+ str(self.time.hours)+ ":"+ str(self.time.minutes) +":"+ str(self.time.seconds)
        self.message(self.time.get_timestamp(), tcod.red)
        self.player.reset()


    def get_input(self):

        key = tcod.console_wait_for_keypress(True)

        if key.vk in mKeys:

            movex,movey = 0,0
            print (movex,movey, key.vk)
            movex, movey = self.get_direction2(key)


            self.player_move(movex,movey)



        elif tcod.console_is_key_pressed(tcod.KEY_ESCAPE):
            return False

        elif tcod.console_is_key_pressed(tcod.KEY_SPACE):
            print "Some Screen"

        else:
            print key.c


    def get_direction(self,key):

        x = 0
        y = 0

        if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
            y = -1
            return x, y
        elif key.vk == tcod.KEY_KP9:
            x = 1
            y = -1
            return x, y
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            x = 1
            return x, y
        elif key.vk == tcod.KEY_KP3:
            x = 1
            y = 1
            return x, y
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
            x = 0
            y = 1
            return x, y
        elif key.vk == tcod.KEY_KP1:
            x = -1
            y = 1
            return x, y
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            x = -1
            return x, y
        elif key.vk == tcod.KEY_KP7:
            x = -1
            y = -1
            return x, y


    def player_move(self,x,y):

        x += self.player.posx
        y += self.player.posy

        if x < 0 or x > MAP_WIDTH or y < 0 or y > MAP_HEIGHT:

            self.change_map(x, y)

        mon = self.mon_at(x, y)
        if mon:
            self.player.hit(mon)
            if mon.hurt():
                self.kill_monster(mon)
            return
        else:
            displace = True

        if self.region.tiles[x][y].movecost > 0:

            self.player.action_points -= self.region.tiles[x][y].movecost

            self.player.posx = x
            self.player.posy = y
            #print self.player.posx, self.player.posy

    def change_map(self,x,y):
        
        if x < 0:
            print "West"
        elif x > MAP_WIDTH:
            print "East"
        elif y < 0: 
            print "North"
        elif y > MAP_HEIGHT:
            print "South"

    def kill_monster(self,mon):

        dead_mon = self.objectBuilder.build_corpse(mon, self.time.tick)
        self.region.objects.append(dead_mon)
        self.region.population.remove(mon)

    def pick_up(self,posx,posy,min):

        object = self.object_at(posx, posy)
        if object:
            print object.name
            self.player.action_points -= 100

    def mon_at(self,x,y):

        for pop in self.region.population:
                if x == pop.posx  and y == pop.posy:
                    return pop

    def object_at(self,x,y):

        for object in self.region.objects:
            if x == object.posx and y == object.posy:
                return object


    def to_camera_coordinates(self,x, y):
        #convert coordinates on the map to coordinates on the screen
        (x, y) = (x - upperLeftX, y - upperLeftY)

        if (x < 0 or y < 0 or x >= CAMERA_WIDTH or y >= CAMERA_HEIGHT):
            return (None, None)  #if it's outside the view, return nothing

        return (x, y)


    def draw(self,thing):
        #only show if it's visible to the player
        if tcod.map_is_in_fov(self.fov_map, thing.posx, thing.posy):
            (x, y) = self.to_camera_coordinates(thing.posx, thing.posy)

            if x is not None:
                #set the color and then draw the character that represents this object at its position

                tcod.console_put_char_ex(self.con, x, y, thing.char,thing.color, tcod.BKGND_NONE)


    def population_move(self):

        for monster in self.region.population:

            dead = False
            while monster.moves > 0:

                monster.make_plans2(self.player,self.fov_map,self.region,self.path_map)

                #monster.move()

            if (dead):
                print monster.name, "is dead"

            else:
                if monster.posx > self.region.width or monster.posy > self.region.height:
                    print monster.name, "out of map"

                else:
                    monster.reset_moves()


    """
    def handle_keys(self,key):


        #movement keys


        if tcod.console_is_key_pressed(tcod.KEY_UP) or tcod.console_is_key_pressed(tcod.KEY_KP8):


        elif tcod.console_is_key_pressed(tcod.KEY_DOWN) or tcod.console_is_key_pressed(tcod.KEY_KP2):


        elif tcod.console_is_key_pressed(tcod.KEY_LEFT) or tcod.console_is_key_pressed(tcod.KEY_KP4):


        elif tcod.console_is_key_pressed(tcod.KEY_RIGHT) or tcod.console_is_key_pressed(tcod.KEY_KP6):


        elif tcod.console_is_key_pressed(tcod.KEY_KP1):


        elif tcod.console_is_key_pressed(tcod.KEY_KP7):


        elif tcod.console_is_key_pressed(tcod.KEY_KP9):


        elif tcod.console_is_key_pressed(tcod.KEY_KP3):

"""

    def get_direction2(self,key):

        x = 0
        y = 0

        if tcod.console_is_key_pressed(tcod.KEY_UP) or tcod.console_is_key_pressed(tcod.KEY_KP8):
            y = -1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_KP9):
            x = 1
            y = -1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_RIGHT) or tcod.console_is_key_pressed(tcod.KEY_KP6):
            x = 1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_KP3):
            x = 1
            y = 1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_DOWN) or tcod.console_is_key_pressed(tcod.KEY_KP2):
            x = 0
            y = 1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_KP1):
            x = -1
            y = 1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_LEFT) or tcod.console_is_key_pressed(tcod.KEY_KP4):
            x = -1
            return x, y
        elif tcod.console_is_key_pressed(tcod.KEY_KP7):
            x = -1
            y = -1
            return x, y


    def get_input2(self):

        key = tcod.console_wait_for_keypress(True)


        if tcod.console_is_key_pressed(tcod.KEY_UP) or tcod.console_is_key_pressed(tcod.KEY_KP8):
            self.player_move(0,-1)

        elif tcod.console_is_key_pressed(tcod.KEY_DOWN) or tcod.console_is_key_pressed(tcod.KEY_KP2):
            self.player_move(0,1)

        elif tcod.console_is_key_pressed(tcod.KEY_LEFT) or tcod.console_is_key_pressed(tcod.KEY_KP4):
            self.player_move(-1,0)

        elif tcod.console_is_key_pressed(tcod.KEY_RIGHT) or tcod.console_is_key_pressed(tcod.KEY_KP6):
            self.player_move(1,0)

        elif tcod.console_is_key_pressed(tcod.KEY_KP1):
            self.player_move(-1,1)

        elif tcod.console_is_key_pressed(tcod.KEY_KP7):
            self.player_move(-1,-1)

        elif tcod.console_is_key_pressed(tcod.KEY_KP9):
            self.player_move(1,-1)

        elif tcod.console_is_key_pressed(tcod.KEY_KP3):
            self.player_move(1,1)


        elif tcod.console_is_key_pressed(tcod.KEY_ESCAPE):
            return False

        elif tcod.console_is_key_pressed(tcod.KEY_SPACE):
            print "Some Screen"

        elif tcod.console_is_key_pressed(tcod.KEY_CHAR):




            key_char = chr(key.c)

            if key_char == 'g':
                self.pick_up(self.player.posx, self.player.posy, 1)


        #else:
            #print key.c



















