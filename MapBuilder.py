import libtcodpy as libtcod
from Tile import *
from Monster import Monster
from Globals import *
from Map import *
from Config import rng, Point
from Items import Item, Corpse

class LevelBuilder:

    # Build the map of Tiles
    def buildTerrain(self,width,height):

        # ListObject as Placeholder for the maptiles
        tileMap = [[0
               for x in range(height)]
                   for y in range(width)]

        for x in range(width):
            for y in range(height):
                if libtcod.random_get_int(0, 0, 10) < 2:
                    tileMap[x][y] = Tile(TileType["Plain"])
                else:
                    tileMap[x][y] = Tile(TileType["Field"])
        return tileMap

    # Build a Map of Structures
    def buildStructures(self,width,height):

        strucMap = [[None
                     for x in range(height)]
                         for y in range(width)]

        for x in range(width):
            for y in range(height):
                if libtcod.random_get_int(0, 0, 10) < 0.5:
                    strucMap[x][y] = Structure(StrucType["Tree"])


        return strucMap

    def buildObjects(self,width,height):

        objectMap = [[None
                     for x in range(height)]
                         for y in range(width)]

        return objectMap



    def mergeMap(self,width,height,tileMap,strucMap):
        map = tileMap[:]

        for x in range(width):
            for y in range(height):
                if strucMap[x][y] != None:
                    map[x][y] = strucMap[x][y]

        return map


    def populate(self,region):
        population = []
        entityCount = libtcod.random_get_int(0,1,10)
        for i in range(entityCount):

                place_point = region.free_random_location()

                pickedAnimal = Animals[libtcod.random_get_int(0, 0, len(Animals) -1)]
                entity = Monster(place_point.x,place_point.y,pickedAnimal[0], pickedAnimal[1],pickedAnimal[2], pickedAnimal[3], pickedAnimal[4],pickedAnimal[5],pickedAnimal[6],pickedAnimal[7],pickedAnimal[8],pickedAnimal[9],pickedAnimal[10],pickedAnimal[11])
                population.append(entity)
                #print entity.posx, entity.posy

        return population


    def buildLevel(self,width,height):

        terrainMap = self.buildTerrain(width, height)
        strucMap = self.buildStructures(width, height)

        self.build_room(3, 5, 27, 10, strucMap,terrainMap)
        map = self.mergeMap(width, height, terrainMap, strucMap)

        level = Level(map)

        return level


    def buildArea(self,width,height):

        area = [[0
               for x in range(height)]
                   for y in range(width)]

        for x in range(width):
            for y in range(height):
                area[x][y] = self.buildLevel(120, 120)

        return area


    def build_room(self,x1,y1,x2,y2,strucMap,terrainMap):

        for i in range(x1,x2 +1):
            for j in range(y1,y2 +1):

                if j == y1 or j == y2:
                    strucMap[i][j] = Structure(StrucType["Wall_h"])

                elif i == x1 or i == x2:
                    strucMap[i][j] = Structure(StrucType["Wall_v"])

                else:
                    terrainMap[i][j] = Tile(TileType["Floor"])

        for i in range(y1 + 1, y2 -1):
            strucMap[x1][i] = Structure(StrucType["Wall_v"])
            strucMap[x2][i] = Structure(StrucType["Wall_v"])

        # Build an opening for a door
        x_opening = (x2 - x1) / 2
        y_opening = y2
        strucMap[x_opening][y_opening] = None

    def place_objects(self,region):

        print Items
        objects = []
        objectcount = 4
        for i in range(objectcount):

            place_point = region.free_random_location()
            item_to_place = Items[0]
            thing = Item(item_to_place[0],item_to_place[1],item_to_place[2],item_to_place[3])

            thing.posx = place_point.x
            thing.posy = place_point.y
            objects.append(thing)
            print thing


        return objects



class WorldBuilder:

    def __init__(self):

        self.seed = rng(1000)



class ObjectBuilder:

    # def __init__(self,glyph, name, description,  color):
    def build_object(self,type):

        newItem = Item()
        return newItem

    def build_corpse(self,mon,tick):

        newCorpse = Corpse(mon.name,mon.color,mon.weight,mon.type,tick)
        newCorpse.posx = mon.posx
        newCorpse.posy = mon.posy
        return newCorpse



















