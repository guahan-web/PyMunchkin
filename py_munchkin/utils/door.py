class DoorCard:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.modifiers = {
            'revealed': [],
            'combat': [],
            'run-away': [],
            'treasure': [],
        }

    def set_modifier(self, type, handler):
        if self.modifiers.get(type) == None:
            raise Exception('Invalid modifier type')
        self.modifiers[type].append(handler)

    def apply_modifiers(self, type, character, value = None):
        modifiers = self.modifiers.get(type, [])
        for modifier in modifiers:
            value = modifier(value, character)
        return value

class Monster(DoorCard):
    def __init__(self, name, description, level = 1, treasures = 1, earned_levels = 1):
        super().__init__(name, description)
        self.level = level
        self.treasures = treasures
        self.earned_levels = earned_levels
        self.bad_stuff = None

    def __str__(self):
        text = """
{name}
{description}
Level: {level}
{bad_stuff}
"""
        return text.format(
            name=self.name,
            description=self.description,
            level=self.level,
            bad_stuff='Bad Stuff: {}'.format(self.bad_stuff['info']) if self.bad_stuff else '',
        )
    
    def set_bad_stuff(self, description, action):
        self.bad_stuff = {
            'info': description,
            'action': action
        }

class Curse(DoorCard):
    def __init__(self, name, description):
        super().__init__(name, description)
