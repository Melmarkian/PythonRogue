from Config import Point,rng
import math

class Level:

    type = ""

    terrain = []
    struc = []
    height = 0
    width = 0

    population = []
    objects = []

    def __init__(self, tiles):
        # Needs a 2d list
        self.tiles = tiles

        self.height = len(tiles[0])
        self.width = len(tiles)


    def move_cost(self,x,y):

        return self.tiles[x][y].movecost


    def free_random_location(self):

        free_locations = []

        for x in range(self.width -1 ):
            for y in range(self.height -1 ):

                if self.move_cost(x,y) > 0:
                    freepoint = Point(x,y)
                    free_locations.append(freepoint)


        return free_locations[rng(0,len(free_locations))]


    def distance(self,start_x,start_y, target_x, target_y):
        #return the distance to some coordinates
        return math.sqrt((target_x - start_x) ** 2 + (target_y - start_y) ** 2)

    


    """
    def sees(self,start_x,start_y,target_x,target_y,range,t):

        dx = start_x - target_x
        dy = start_y - target_y

        ax = math.fabs(dx) / 2
        ay = math.fabs(dy) / 2

        if dx < 0:
            sx = -1
        else:
             sx = 1

        if dy < 0:
            sy = -1
        else:
             sy = 1


        t = 0


        if range > 0 and (math.fabs(dx) > range or math.fabs(dy) > range):
            return False
        if ax > ay:
            thing = ay - (ax / 2)

            if thing < 0:
                st = -1
            else:
                st = 1


            for (tc = math.fabs(ay - (ax /2)) * 2 + 1; tc >= -1; tc +=1):

                t = tc * st
"""






























