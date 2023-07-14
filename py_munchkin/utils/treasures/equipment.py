from py_munchkin.utils.items import *

# generate all our weapons
def generateWeapons():
    weapons = []

    item = Weapon(
        name='Eleven-Foot Pole',
        value=200, 
        bonus=1,
        dual_weild=True
    )
    weapons.append(item)

    item = Weapon(
        name='Rapier of Unfairness',
        value=600,
        description='Usable by Elf Only',
        bonus=3
    )
    item.set_restriction(lambda character: character.race == 'elf')
    weapons.append(item)

    item = Weapon(
        name='Chainsaw of Bloody Dismemberment',
        value=600,
        is_large=True,
        dual_weild=True,
        bonus=3
    )
    weapons.append(item)

    item = Weapon(
        name='Swiss Army Polearm',
        value=600,
        description='Usable by Human Only',
        is_large=True,
        dual_weild=True,
        bonus=4
    )
    item.set_restriction(lambda character: character.race == 'human')
    weapons.append(item)

    return weapons

# generate armor
def generateArmor():
    armor = []

    item = Armor(
        name='Flaming Armor',
        value=400,
        bonus=2
    )
    armor.append(item)

    return armor

# generate headgear
def generateHeadgear():
    headgear = []

    item = Headgear(
        name='Helm of Courage',
        value=200,
        bonus=1
    )
    headgear.append(item)

    return headgear

# generate footgear
def generateFootgear():
    footgear = []

    item = Footgear(
        name='Boots of Running Really Fast',
        value=400,
        description='Gives you +2 to Run Away',
        bonus=0
    )
    item.set_modifier('run-away', lambda x: x + 2)
    footgear.append(item)

    return footgear

def generateAllEquipmentCards():
    cards = generateWeapons() + generateArmor() + generateHeadgear() + generateFootgear()
    return cards
