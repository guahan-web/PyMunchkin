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
        self.die = Die(6)

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
            print('Attempting to run away...')
            # monster wins, must attempt to run away
            roll = monster.apply_modifiers('run-away', self.die.roll(), self.character)
            print('FYI, effective roll: {}'.format(roll))
            if roll < 5:
                # failure
                print('Out of luck!')
                self.character.levelDown() # default to losing one level
            else:
                # success
                print('You survived to fight another day!')
        

    def showHand(self):
        for card in self.hand:
            card.show()

