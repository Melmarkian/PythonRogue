import libtcodpy as libtcod

t_wall_h = libtcod.CHAR_HLINE
t_wall_v = libtcod.CHAR_VLINE
t_tree   = libtcod.CHAR_ARROW_N

# Map Tiles with properties
Field = {"glyph" : '.',
         "desc" : "This is a Field",
         "charColor" : libtcod.dark_green,
         "backColor" : libtcod.black,
         "movecost": 100,
         "block_sight": False
        }

Wall =  {"glyph" : '#',
         "desc" : "This is a Wall",
         "charColor" : libtcod.white,
         "backColor" : libtcod.black,
         "movecost": 0,
         "block_sight": True
        }

Plain = {"glyph" : '.',
         "desc" : "Sandy Plains",
         "charColor": libtcod.dark_amber,
         "backColor": libtcod.black,
         "movecost": 100,
         "block_sight": False
         }

Floor = {"glyph" : '.',
         "desc" : "Floor",
         "charColor": libtcod.white,
         "backColor": libtcod.black,
         "movecost": 100,
         "block_sight": False
         }



TileType = { "Field" : Field,
             "Wall": Wall,
             "Plain": Plain,
             "Floor": Floor

            }


Wall_v = {"glyph" : t_wall_v,
          "desc" :  "Wall",
          "charColor" : libtcod.white,
          "backColor" : libtcod.black,
          "hp" : 60,
          "armor" : 10,
          "movecost" : 0,
          "block_sight" : True
          }

Wall_h = {"glyph" : t_wall_h,
          "desc" :  "Wall",
          "charColor" : libtcod.white,
          "backColor" : libtcod.black,
          "hp" : 60,
          "armor" : 10,
          "movecost" : 0,
          "block_sight" : True
          }


Tree = {"glyph" : "^",
         "desc" : "A nice Tree",
         "charColor" : libtcod.green,
         "backColor" : libtcod.black,
         "hp": 40,
         "armor": 4,
         "movecost": 0,
         "block_sight": True
         }

StrucType = { "Tree": Tree,
              "Wall_h" : Wall_h,
              "Wall_v" : Wall_v
             }

class Tile:
    #a tile of the map and its properties
    def __init__(self, type):

        self.glyph = type["glyph"]
        self.desc = type["desc"]
        self.charColor = type["charColor"]
        self.backColor = type["backColor"]
        self.movecost = type["movecost"]
        self.block_sight = type["block_sight"]
        self.explored = False

class Structure:
    #A Structure on the map
    def __init__(self,type):

        self.glyph = type["glyph"]
        self.desc = type["desc"]
        self.charColor = type["charColor"]
        self.backColor = type["backColor"]
        self.hp = type["hp"]
        self.armor = type["armor"]
        self.movecost = type["movecost"]
        self.block_sight = type["block_sight"]
        self.explored = False

