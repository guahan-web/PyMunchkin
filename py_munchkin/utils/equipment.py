class Item:
    def __init__(self, name, value, description = '', is_large = False):
        self.is_large = is_large
        self.restrictions = []
        self.name = name
        self.description = description
        self.value = value
        self.modifiers = {
            'combat': [],
            'run-away': [],
        }

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
    def __init__(self, name, value, description = '', is_large = False):
        super().__init__(name, value, description, is_large)
        # for testing, let's just constrain one piece of headgear
        self.set_restriction(lambda character: (not character.hasHeadgear()))

class Footgear(Item):
    def __init__(self, name, value, description = '', is_large = False):
        super().__init__(name, value, description, is_large)
        # for testing, let's just constrain one piece of footgear
        self.set_restriction(lambda character: (not character.hasFootgear()))

class Weapon(Item):
    def __init__(self, name, value, description = '', is_large = False, dual_weild = False):
        super().__init__(name, value, description, is_large)
        self.dual_weild = dual_weild
