from py_munchkin.utils.character import Character
from py_munchkin.utils.die import Die
from py_munchkin.utils.monster import Monster

class Player:
    def __init__(self, name = 'Player 1'):
        self.level = 1
        self.turn_number = 0
        self.name = name
        self.hand = []
        self.character = Character()

    def drawCard(self, deck):
        self.hand.append(deck.drawCard())

    def kickOpenTheDoor(self, door_deck):
        print('Player kicked open the door!')
        card = door_deck.drawCard()

        # be sure to handle properly
        if isinstance(card, Monster):
            self.resolveBattle(card)
        else:
            print('still to come... curses and items...')

    def resolveBattle(self, monster):
        cLevel = self.character.getEffectiveLevel()
        mLevel = monster.apply_modifiers('combat', monster.level, self.character)

        print('A monster was waiting!')
        print(str(monster))

        print('Effective level: {}'.format(cLevel))
        print('Monster strength: {}'.format(mLevel))
        print()

        if cLevel > mLevel:
            # player wins, raid the treasure
            treasures = monster.apply_modifiers('treasure', monster.treasures, self.character)
            print('Collect {} treasures!'.format(treasures))
        else:
            # monster wins, must attempt to run away
            escaped = self.runAway()
            escaped = monster.apply_modifiers('run-away', escaped, self.character)
            if escaped == True:
                # success
                print('You survived to fight another day!')
            else:
                # failure
                print('Out of luck!')
                self.character.levelDown() # default to losing one level
        

    # action that requires rolling a 5 or 6 on a 6-sided die
    def runAway(self):
        die = Die(6)
        return (die.roll() >= 5)

    def showHand(self):
        for card in self.hand:
            card.show()

