from py_munchkin.utils.door import Curse
from py_munchkin.utils.items import *

def loseAllFootgear(character):
    gear = character.getEquipmentByType(Footgear)
    if gear:
        character.unequipItem(gear)
    return gear


def generateAllCurseCards():
    curses = []

    curse = Curse('Curse!', 'Lose the footgear you are wearing')
    curse.set_modifier('revealed', loseAllFootgear)
    curses.append(curse)

    return curses