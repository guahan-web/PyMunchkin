class Character:
    def __init__(self):
        self.base_level = 1
        self.equipment = []
        self.gold = 0

    def __str__(self):
        text="""Character info:
    level: {level}
    attack: {attack}
    equipment: {equipment}
    gold: {gold}
"""

        return text.format(
            level=self.base_level,
            attack=self.getAttackPower(),
            equipment=len(self.equipment),
            gold=self.gold
        )

    def levelUp(self):
        self.base_level += 1

    def sellItem(self, item):
        # will raise an exception if not equipped
        self.equipment.remove(item)
        self.gold += item.value

    def equipItem(self, item):
        self.equipment.append(item)

    def getAttackPower(self):
        pow = self.base_level
        for item in self.equipment:
            pow = item.apply_modifiers('attack', pow)
        return pow
