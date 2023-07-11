import argparse
from py_munchkin.utils.die import *
from py_munchkin.utils.cards import Deck
from py_munchkin.utils.player import Player
from py_munchkin.utils.game import Game

# example of some game stuff
def startGame(args):
    game = Game(4) # max players: 4
    game.addPlayer('Foo')
    game.addPlayer('Bar')
    game.addPlayer('Fizz')
    game.addPlayer('Buzz')

    # cannot add a 5th player
    try:
        game.addPlayer('Baz') # should fail
    except Exception as e:
        print('Error: ' + str(e))

    # set up some event listeners
    def printEvent(e): print("event received: {}".format(e))
    game.events.add_listener('game-start', printEvent)
    game.events.add_listener('round-start', printEvent)
    game.events.add_listener('round-end', printEvent)
    game.events.add_listener('player-turn', printEvent)

    # run through two full turn cycles to test
    game.start()
    game.nextTurn()
    game.nextTurn()
    game.nextTurn()
    game.nextTurn()
    game.nextTurn()
    game.nextTurn()
    game.nextTurn()

# example of some card stuff
def drawCards(args):
    deck = Deck()
    deck.shuffle()

    player = Player()
    for _ in range(5): # draw 5 cards
        player.drawCard(deck)

    player.showHand()
    
# dice rolling
def roll(args):
    if args.multi:
        dice = Dice(6, 6, 6) # 3 6-sided dice
        value = dice.roll()
        print(value)
    else:
        die = Die(args.sides)
        value = die.roll()
        print("Dice roll: %d" % (value))

# main program
def main():
    parser = argparse.ArgumentParser(description="Munchkin")
    # Add your CLI commands, options, and arguments here

    # Create parser for the "roll" command
    subparsers = parser.add_subparsers(help='sub-command help')

    roll_parser = subparsers.add_parser('roll', help='roll help')
    roll_parser.add_argument('-s', '--sides', type=int, default=6, help='--sides help')
    roll_parser.add_argument('-m', '--multi', action='store_true')
    roll_parser.set_defaults(func=roll)

    card_parser = subparsers.add_parser('draw', help='draw help')
    card_parser.set_defaults(func=drawCards)

    game_parser = subparsers.add_parser('game', help='game help')
    game_parser.set_defaults(func=startGame)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
