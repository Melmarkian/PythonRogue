class Item:

    name = ""
    description = "generic Item description"


    carried = False
    posx, posy = 0,0

    hp = 10
    quality = 100





    def __init__(self,glyph, name, description,  color):

        self.name = name
        self.description = description
        self.char = glyph
        self.color = color


class Corpse(Item):

    def __init__(self,name, color, weight, type, tick):

        self.char = "%"
        self.name = name + " corpse"
        self.description = "This is a " + name + " corpse."
        self.color = color
        self.weight = weight
        self.type = type
        self.bday = tick

    def butcher(self, skilltest = 100 ):

        if self.type == "Mammal":
            flesh = 0.1 + self.weight * (float(skilltest) / 100)
            bone = self.weight * (float(skilltest) / 300)




class Food:

    def __init__(self,char,name,description,color,weight,type,tick):

        self.char = char
        self.name = name
        self.description = description
        self.color = color
        self.weight = weight
        self.type = type
        self.bday = tick








