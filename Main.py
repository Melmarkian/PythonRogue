from Game import Game

# Do the game
#

if __name__ == '__main__':

    plays = True

    game = Game()
    game.new_game()

    print (len(game.region.population))

    while plays:
        game.do_turn()


