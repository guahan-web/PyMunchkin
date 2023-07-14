from py_munchkin.utils.character import Character
from py_munchkin.utils.die import Die
from py_munchkin.utils.door import Monster

class Player:
    def __init__(self, name = 'Player 1'):
        self.level = 1
        self.turn_number = 0
        self.name = name
        self.hand = []
        self.character = Character()
        self.die = Die(6)

    def drawCard(self, deck):
        card = deck.drawCard()
        if card:
            self.hand.append(card)

    def showHand(self):
        print('Current Hand:')
        for x in self.hand:
            print(' - {name} ({bonus}){description}'.format(
                name=x.name,
                bonus=('+' + str(x.bonus) + ' BONUS') if x.bonus > 0 else 'no bonus',
                description=(': ' + x.description) if x.description != '' else '',
            ))

