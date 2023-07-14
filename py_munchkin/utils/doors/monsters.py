from py_munchkin.utils.door import Monster

def generateAllMonsterCards():
    monsters = []

    # Level 1
    monster = Monster('Potted Plant', 'Elves draw an extra Treasure after defeating it')
    monster.set_modifier('treasure', lambda x, character: x + 1 if character.race == 'elf' else x)
    monster.set_modifier('run-away', lambda x, character: 6) # automatically roll a 6 (automatic escape)
    monsters.append(monster)

    monster = Monster('Maul Rat', '+3 against Clerics')
    monster.set_modifier('combat', lambda pow, character: pow + 3 if character.cclass == 'cleric' else pow)
    monsters.append(monster)

    monster = Monster('Lame Goblin', '')
    monster.set_modifier('run-away', lambda x, character: x + 1)
    monsters.append(monster)

    # Level 2
    monster = Monster('Monster Under the Bed', '+2 against Halflings and Dwarves.', 2)
    monster.set_modifier('combat', lambda pow, character: pow + 2 if character.race in ['halfling', 'dwarf'] else pow)
    monster.set_bad_stuff(
        'Something rolls under the bed and you\'re afraid to look for it. Discard one small item.',
        lambda character: print('discarding an item...'),
    )
    monsters.append(monster)

    # Level 8
    monster = Monster('Gazebo', 'No one can help you. You must face the Gazebo alone.', 8, 2)
    # todo: set up bad stuff:
    # Lose 3 levels
    monsters.append(monster)

    # Level 10
    monster = Monster('3,872 Orcs', '+6 against Dwarves, due to ancient grudges', 10, 3)
    # todo: set up bad stuff:
    # Roll a die. On a 2 or less, they stomp you to death. Otherwise, lose as many levels as the die shows.
    monsters.append(monster)

    # Level 18
    monster = Monster(
        name='Squidzilla',
        description='Slimy! Elves are at -4! Will not pursue anyone of Level 4 or below except Elves.',
        level=18,
        treasures=4,
        earned_levels=2
    )
    monster.set_modifier('combat', lambda pow, character: pow - 4 if character.race == 'elf' else pow)
    monster.set_modifier('run-away', lambda x, character: x if character.race == 'elf' else 6) # no pursuit
    # todo: set up the bad stuff:
    # You are grabbed, slimed, crushed, and gobbled. You are dead, dead, dead. Any questions?
    monsters.append(monster)

    # Level 20
    monster = Monster(
        name='Plutonium Dragon',
        description='Will not pursue anyone of Level 5 or below.',
        level=20,
        treasures=5,
        earned_levels=2
    )
    monster.set_modifier('run-away', lambda x, character: x if character.base_level > 5 else 6) # no pursuit if level <= 5
    monsters.append(monster)

    return monsters
