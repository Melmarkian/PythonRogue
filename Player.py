import libtcodpy as tcod

class Player:

    char = '@'
    name = "Player"
    color = tcod.white
    posx = 20
    posy = 20

    # Primary
    strength = 0
    toughness = 0
    speed = 0
    senses = 0
    logic = 0
    social = 0

    # Secondary
    action_points = 100
    sight = 10 + senses
    carry_capacity = 20
    carry_overweight_step = carry_capacity / 10
    damage_reduction = (toughness + (strength / 5)) / 10

    # Food n stuff
    hunger = 0



    # Skills
    butchery = 100

    def reset(self):

        self.action_points += 100


    def hit(self,mon):
        print "Hit " + mon.name













