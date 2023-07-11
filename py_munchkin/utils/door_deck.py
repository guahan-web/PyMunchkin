import random
from py_munchkin.utils.monster import Monster

class DoorDeck:
    def __init__(self):
        self.cards = []

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()

def generateDoorDeck():
    deck = DoorDeck()

    plant = Monster('Potted Plant', 'Elves draw an extra Treasure after defating it')
    plant.set_modifier('treasure', lambda x, character: x + 1 if character.race == 'elf' else x)
    plant.set_modifier('run-away', lambda x, character: 6) # automatically roll a 6 (automatic escape)

    rat = Monster('Maul Rat', '+3 against Clerics')
    rat.set_modifier('combat', lambda pow, character: pow + 3 if character.cclass == 'cleric' else pow)

    goblin = Monster('Lame Goblin', '')
    goblin.set_modifier('run-away', lambda x, character: x + 1)

    deck.cards.append(plant)
    deck.cards.append(rat)
    deck.cards.append(goblin)
    deck.shuffle()
    return deck