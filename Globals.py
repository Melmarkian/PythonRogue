import libtcodpy as tcod
# Stuff (Important)
fov_recompute = True
turns = 0
BASE_TIME = 20

# Movement Keys
mKeys = (tcod.KEY_DOWN, tcod.KEY_UP, tcod.KEY_RIGHT, tcod.KEY_LEFT,
         tcod.KEY_KP1, tcod.KEY_KP2, tcod.KEY_KP3, tcod.KEY_KP4,
         tcod.KEY_KP6, tcod.KEY_KP7, tcod.KEY_KP8, tcod.KEY_KP9)

# Tiles

# Bodyparts
Head = ()
Thorax = ()
Abdomen = ()
Arm = ()
Leg = ()

# Types of Bodys
FourLegged =   ((Head,1),(Thorax,1),(Abdomen,1),(Leg,4))
Snake =        ((Head,1),(Thorax,1),(Abdomen,1))
Humanoid =     ((Head,1),(Thorax,1),(Abdomen,1),(Arm,2),(Leg,2))

# To Hit
FourLegged = ()
Snake =      ()
Humanoid =   ()



# Monsters
#         char   NameString          color              speed                 type     Size weight   hp    melee,dodge,range
Animals = (

    (    "d",    "Wild dog",         tcod.copper,       120,    FourLegged,   "Mammal", 4,    30,    20,    70,30,-1),
    (    "s",    "Snake",            tcod.green,        60,     Snake,        "Lizard", 2,    2,     10,    70,20,-1),
    (    "b",    "Boar",             tcod.darker_amber, 110,    FourLegged,   "Mammal", 5,    45,    25,    80,20,-1)

    )






Items = (

    (    tcod.CHAR_DTEEW,    "Flesh",    "raw flesh",    tcod.red,        0.1),
    ()



         )




