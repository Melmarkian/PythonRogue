import libtcodpy as tcod
import math

class Monster:

    def __init__(self,posx,posy,char,name,color,speed,body,type,size,weight,hp,melee,dodge,range):

        self.posx = posx
        self.posy = posy

        self.char = char
        self.name = name
        self.color = color
        self.blocks = True

        self.speed = speed
        self.moves = speed
        self.type = type
        self.body = body
        self.size = size
        self.weight = weight
        self.sightrange = 10

        self.hp = hp
        self.melee = melee
        self.dodge = dodge
        self.range = range

        self.count = 0
        self.has_seen = False
        self.plan = None
        self.behaviour = "Hostile"
        self.preyx = -1
        self.preyy = -1


    def say_name(self):

        print self.name

    def get_sight(self):
        return self.sightrange

    def make_plans(self,player,fov_map,region):

        if tcod.map_is_in_fov(fov_map, self.posx,self.posy):
            self.has_seen = True
            self.sees_player = True
        else:
            self.sees_player = False



        if self.distance_to(player) == 1:

            print self.name, "hits you"


        elif (self.plan == None and self.sees_player):

            # If not next to the player and inside the player fov, set the path with the player as destination
            if self.distance_to(player) >= 2 and tcod.map_is_in_fov(fov_map, self.posx,self.posy):

                self.set_dest(fov_map, player.posx, player.posy)

        elif self.plan == None:

            location = region.free_random_location()
            self.set_dest(fov_map, location.x,location.y)

    def make_plans2(self,player,fov_map,region,path_map):

        if self.behaviour == "Hostile":

            tcod.map_compute_fov(fov_map, self.posx, self.posy, self.get_sight(), True ,0)

            if tcod.map_is_in_fov(fov_map, player.posx, player.posy):

                if tcod.path_compute(path_map,self.posx,self.posy,player.posx,player.posy):
                    self.preyx = player.posx
                    self.preyy = player.posy
                    x,y = tcod.path_walk(path_map, True)
                    if not x is None:
                        if x == player.posx and y == player.posy:
                            print self.name, "hits you!"
                            self.moves -= 100
                        else:
                            self.posx = x
                            self.posy = y
                            self.moves -= 100
                    else:
                        self.moves = 0


            # Doesnt see player but has seen him
            elif self.preyx > 0:

                if tcod.path_compute(path_map,self.posx,self.posy,self.preyx,self.preyy):
                    x,y = tcod.path_walk(path_map, True)
                    if not x is None:
                        self.posx = x
                        self.posy = y
                        self.moves -= 100
                    else:
                        self.moves = 0

            else:
                self.moves = 0


    def set_dest(self,fov_map,x,y):

       path = tcod.path_new_using_map(fov_map,  1.0)
       tcod.path_compute(path,self.posx,self.posy,x,y)

       self.plan = path


    def reset_moves(self):

        self.moves += self.speed


    def move(self):

        #print tcod.path_get_destination(self.plan)
        if self.plan and not tcod.path_is_empty(self.plan):
            x,y = tcod.path_walk(self.plan,True)
            self.posx = x
            self.posy = y
            self.moves -= 100

        else:
            self.plan = None
            self.moves = 0



    def distance_to(self, other):
        #return the distance to another object
        dx = other.posx - self.posx
        dy = other.posy - self.posy
        return math.sqrt(dx ** 2 + dy ** 2)

    def die(self,tick):
        print "I die!"



    def hurt(self):


        return True









