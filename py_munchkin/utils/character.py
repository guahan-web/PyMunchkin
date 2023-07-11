from py_munchkin.utils.equipment import *

MAX_HANDS = 2
LEVEL_COST = 1000

class Character:
    def __init__(self):
        self.base_level = 1
        self.equipped = []
        self.carrying = []
        self.gold = 0
        self.race = None
        self.cclass = None

    def __str__(self):
        text="""Character info:
    level: {level}
    race: {race}
    class: {cclass}
    combat: {combat}
    equipment: {equipment}
    carrying: {carrying}
    gold: {gold}
"""

        return text.format(
            level=self.base_level,
            race=self.race,
            cclass=self.cclass,
            combat=self.getEffectiveLevel(),
            equipment=len(self.equipped),
            carrying=len(self.carrying),
            gold=self.gold
        )

    # increase character level by X
    def levelUp(self, level = 1):
        self.base_level += level

    # decrease character level by X
    def levelDown(self, level = 1):
        self.base_level -= level

    # if an item is in inventory, trade it for gold
    def sellItem(self, item):
        if item in self.carrying:
            self.carrying.remove(item)
            self.gold += item.value
        elif item in self.equipped:
            self.equipped.remove(item)
            self.gold += item.value
        else:
            raise Exception('Provided item is not in inventory')

    # place item "on table" without equipping it
    def carryItem(self, item):
        if item.is_large and self.hasBigItem():
            raise Exception('Already carrying a large item')
        self.carrying.append(item)

    # equip an item
    def equipItem(self, item):
        if not item.canBeEquipped(self):
            raise Exception('Your character cannot equip this item')

        # first, be sure we aren't breaking large item rule
        if item.is_large and self.hasBigItem():
            raise Exception('Already carrying a large item')

        # now, be sure we have enough hands free for this weapon
        if isinstance(item, Weapon):
            # check to be sure we have enough free hands
            available = self.getHandsAvailable()
            if (available < 1) or (item.dual_weild and available < 2):
                raise Exception('Not enough hands free to equip')

        # finally, actually equip the item
        self.equipped.append(item)

    # remove an item from equipment list
    def unequipItem(self, item):
        if item not in self.equipped:
            raise Exception('Character does not have this item equipped')
        self.equipped.remove(item)

    # if there is enough gold, trade it for a level
    def buyLevel(self):
        if self.gold < LEVEL_COST:
            raise Exception('Not enough gold to buy a level')
        self.gold -= LEVEL_COST
        self.levelUp()

    # check for a big item
    def hasBigItem(self):
        for i in self.equipped:
            if i.is_large: return True

        for i in self.carrying:
            if i.is_large: return True

        return False
    
    def hasHeadgear(self):
        for i in self.equipped:
            if isinstance(i, Headgear): return True
        return False
    
    def hasFootgear(self):
        for i in self.equipped:
            if isinstance(i, Footgear): return True
        return False

    # based see how many hands we have free
    # TODO: figure out how race exceptions can apply
    def getHandsAvailable(self):
        available = MAX_HANDS
        for w in self.equipped:
            if isinstance(w, Weapon):
                available -= 1
                if w.dual_weild: available -= 1
        return available
    
    # calculate attack power based on base level
    def getEffectiveLevel(self, penalties = []):
        level = self.base_level
        for item in self.equipped:
            level = item.apply_modifiers('combat', level)
        # if penalties provided, honor them
        for p in penalties:
            level = p(level)
        return level
