class Item:
    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.modifiers = {
            'attack': [],
            'run-away': [],
        }

    def set_modifier(self, type, handler):
        if self.modifiers.get(type) == None:
            raise Exception('Invalid modifier type')
        self.modifiers[type].append(handler)

    def apply_modifiers(self, type, value):
        modifiers = self.modifiers.get(type, [])
        for modifier in modifiers:
            value = modifier(value)
        return value


class Headgear(Item):
    def __init__(self, name, value):
        super().__init__(name, value)

class Armor(Item):
    def __init__(self, name, value):
        super().__init__(name, value)

class Footgear(Item):
    def __init__(self, name, value):
        super().__init__(name, value)

class Weapon(Item):
    def __init__(self, name, value, description, dual_weild = False):
        super().__init__(name, value, description)
        self.dual_weild = dual_weild
