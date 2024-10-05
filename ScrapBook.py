# Working population
def populate(self,region):
        population = []
        entityCount = libtcod.random_get_int(0,1,10)
        for i in range(entityCount):
            x = libtcod.random_get_int(0, 0, region.width -1)
            y = libtcod.random_get_int(0,0,region.height -1)

            if region.tiles[x][y].movecost > 0:

                pickedAnimal = Animals[libtcod.random_get_int(0, 0, len(Animals) -1)]
                entity = Monster(x,y,pickedAnimal[0], pickedAnimal[1],pickedAnimal[2], pickedAnimal[3], pickedAnimal[4])
                population.append(entity)
                print entity.posx, entity.posy

        return population








