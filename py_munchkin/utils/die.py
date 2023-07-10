import random

class Die:
    def __init__(self, sides = 6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)
    
class Dice:
    def __init__(self, *argv):
        list = []
        for arg in argv:
            sides = int(arg)
            list.append(Die(sides))
            self.dice = list
                
    def roll(self):
        dice = []
        total = 0

        for die in self.dice:
            value = die.roll()
            dice.append(value)
            total += value

        return {'dice': dice, 'total': total}
