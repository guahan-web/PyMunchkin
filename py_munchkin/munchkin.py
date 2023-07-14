import argparse
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from py_munchkin.utils.die import *
from py_munchkin.utils.cards import Deck
from py_munchkin.utils.player import Player
from py_munchkin.utils.game import Game
from py_munchkin.utils.items import *

def runDemo(args):
    # for demo, hard-code a list of options
    races = ['elf', 'human', 'dwarf', 'halfling', 'orc', 'gnome']
    classes = ['cleric', 'wizard', 'warrior', 'thief', 'bard', 'ranger']

    # prompt the user to select a race
    selected_race = inquirer.select(
        message='Select a race:',
        choices=map(lambda race: Choice(race, name=race.capitalize()), races),
        default=None,
    ).execute()

    # prompt the user to select a class
    selected_class = inquirer.select(
        message='Select a character class:',
        choices=map(lambda c: Choice(c, name=c.capitalize()), classes),
        default=None,
    ).execute()

    # set up a new game and test a couple actions
    game = Game()

    player = Player()
    player.character.cclass = selected_class
    player.character.race = selected_race

    game.addPlayer(player)
    game.start() # start the turn cycle

    # for demo purposes, give a choice of three random items to equip
    demo_items = [
        game.treasures.drawCard(),
        game.treasures.drawCard(),
        game.treasures.drawCard(),
    ]

    selected_item = inquirer.select(
        message='Select a starting item:',
        choices=[
            Choice(i, '{name} ({bonus}){description}'.format(
                name=x.name,
                bonus=('+' + str(x.bonus) + ' BONUS') if x.bonus > 0 else 'no bonus',
                description=(': ' + x.description) if x.description != '' else '',
            )) for i,x in enumerate(demo_items)
        ]
    ).execute()

    # clean up demo items (discard unselected)
    for i in range(len(demo_items)):
        if i == selected_item:
            try:
                item = demo_items[selected_item]
                player.character.equipItem(item)
                color_print([('#1fb82e', 'Equipped: '), ('#ffffff', item.name)])
            except Exception as e:
                color_print([('#e5c07b', 'Poor choice: '), ('#ffffff', str(e))])
        else:
            game.discardCard(demo_items[i])
    demo_items.clear()

    # start the first phase of your turn
    game.kickOpenDoor()

    # show the summary of the character now
    print()
    print(str(player.character))
    player.showHand()

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
    deck.build()
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

    character_parser = subparsers.add_parser('demo', help='demo help')
    character_parser.set_defaults(func=runDemo)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
