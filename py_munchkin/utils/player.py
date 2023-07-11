class Player:
    def __init__(self, name = 'Player 1'):
        self.level = 1
        self.turn_number = 0
        self.name = name
        self.hand = []

    def drawCard(self, deck):
        self.hand.append(deck.drawCard())

    def showHand(self):
        for card in self.hand:
            card.show()

