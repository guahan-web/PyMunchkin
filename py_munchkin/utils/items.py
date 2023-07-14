class Item:
    def __init__(self, name, value, description = '', bonus = 1, is_large = False):
        self.is_large = is_large
        self.restrictions = []
        self.name = name
        self.description = description
        self.bonus = bonus
        self.value = value
        self.modifiers = {
            'combat': [],
            'run-away': [],
        }
        self.set_modifier('combat', lambda x: x + bonus)

    def __str__(self):
        text="""Item info:
    {bonus}
    name: {name}
    description: {description}
    large: {large}
    value: {gold} Gold
"""
        return text.format(
            bonus = ('+' + str(self.bonus) + ' BONUS') if self.bonus > 0 else 'no bonus',
            name = self.name,
            description = self.description,
            large = 'yes' if self.is_large else 'no',
            gold = self.value,
        )
        

    def set_large_item(self, is_large = True):
        self.is_large = is_large

    def set_modifier(self, type, handler):
        if self.modifiers.get(type) == None:
            raise Exception('Invalid modifier type')
        self.modifiers[type].append(handler)

    def apply_modifiers(self, type, value):
        modifiers = self.modifiers.get(type, [])
        for modifier in modifiers:
            value = modifier(value)
        return value
    
    def set_restriction(self, restriction):
        self.restrictions.append(restriction)
    
    def canBeEquipped(self, character):
        for r in self.restrictions:
            if not r(character): return False
        return True

class Headgear(Item):
    def __init__(self, name, value, description = '', bonus = 1, is_large = False):
        super().__init__(name, value, description, bonus, is_large)
        # for testing, let's just constrain one piece of headgear
        self.set_restriction(lambda character: (not character.hasHeadgear()))

class Footgear(Item):
    def __init__(self, name, value, description = '', bonus = 1, is_large = False):
        super().__init__(name, value, description, bonus, is_large)
        # for testing, let's just constrain one piece of footgear
        self.set_restriction(lambda character: (not character.hasFootgear()))

class Armor(Item):
    def __init__(self, name, value, description = '', bonus = 1, is_large = False):
        super().__init__(name, value, description, bonus, is_large)
        # for testing, let's just constrain one piece of armor
        self.set_restriction(lambda character: (not character.hasArmor()))

class Weapon(Item):
    def __init__(self, name, value, description = '', bonus = 1, is_large = False, dual_weild = False):
        super().__init__(name, value, description, bonus, is_large)
        self.dual_weild = dual_weild
