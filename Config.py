import libtcodpy as tcod

def rng(start = 0,finish = 100):

    number = tcod.random_get_int(0,start,finish)

    return number

class Point:

    def __init__(self,x,y):

        self.x = x
        self.y = y

    def getPos(self):

        return self.x,self.y































