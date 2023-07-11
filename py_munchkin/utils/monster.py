class Monster:
    def __init__(self, name, description, level = 1, treasures = 1, earned_levels = 1):
        self.name = name
        self.description = description
        self.level = level
        self.treasures = treasures
        self.earned_levels = earned_levels
        self.bad_stuff = None
        self.modifiers = {
            'combat': [],
            'run-away': [],
            'treasure': []
        }

    def __str__(self):
        text = """
{name}
{description}
Level: {level}
"""
        return text.format(name=self.name, description=self.description, level=self.level)

    def set_modifier(self, type, handler):
        if self.modifiers.get(type) == None:
            raise Exception('Invalid modifier type')
        self.modifiers[type].append(handler)

    def apply_modifiers(self, type, value, character):
        modifiers = self.modifiers.get(type, [])
        for modifier in modifiers:
            value = modifier(value, character)
        return value
