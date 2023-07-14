from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from py_munchkin.utils.eventbus import EventBus
from py_munchkin.utils.door import Monster
from py_munchkin.utils.die import Die
from py_munchkin.utils.cards import Deck
from py_munchkin.utils.cards import getDoorDeck
from py_munchkin.utils.cards import getTreasureDeck

class Game:
    def __init__(self, max_players = 4):
        self.events = EventBus()
        self.players = []
        self.current_player = None
        self.max_players = max_players
        self.die = Die() # need a 6-sided die

        # set up door deck
        doors = getDoorDeck()
        doors.shuffle()
        self.doors = doors

        # set up treasure deck
        treasures = getTreasureDeck()
        treasures.shuffle()
        self.treasures = treasures

        # empty discard deck
        self.discard = Deck()
        

    def addPlayer(self, player):
        if len(self.players) >= self.max_players:
            raise Exception('Game already at maximum capacity')

        self.players.append(player)
        
    def start(self):
        if len(self.players) < 1:
            raise Exception('Cannot start a game with no players')
        
        # do any other setup here
        self.events.emit('game-start', "Game Started")
        self.nextTurn()
        
        
    def nextTurn(self):
        if self.current_player == None:
            self.current_player = 0
        elif self.current_player == len(self.players) - 1:
            self.events.emit('round-end', "End of Round")
            self.current_player = 0
        else:
            self.current_player += 1

        if self.current_player == 0:
            self.events.emit('round-start', "Starting Round")

        self.events.emit('player-turn', self.players[self.current_player])

    def kickOpenDoor(self):
        player = self.players[self.current_player]
        card = self.doors.drawCard()

        print('\nYou kicked open the door!')
        if isinstance(card, Monster):
            color_print([
                ('#e5c07b', 'Monster encountered! '),
                ('', 'You discovered a:'),
            ])

            color_print([
                ('#fff', card.name),
                ('', ' (level {})'.format(card.level)),
                ('#00cce3', ' - {}'.format(card.description) if card.description != '' else '')
            ])

            if card.bad_stuff:
                print('Bad Stuff: ' + card.bad_stuff['info'])

            self.resolveBattle(card, player)
        else:
            print('Soon to come: curses, monster enhancers, classes, races, helpers, etc...')

    def resolveBattle(self, monster, player):
        character = player.character
        cLevel = character.base_level + character.getLevelModifier()
        mLevel = monster.apply_modifiers('combat', character, monster.level)

        levelMessage = [
            ('', '\nCharacter level: '),
            ('#fff', str(character.base_level)),
        ]
        modifier = character.getLevelModifier()
        if modifier > 0:
            levelMessage.append(('#1fb82e', ' (+{})'.format(modifier)))
        elif modifier < 0:
            levelMessage.append(('#cf0000', ' (-{})'.format(abs(modifier))))
        
        color_print(levelMessage)

        if cLevel > mLevel:
            # character wins, so let's resolve the results
            color_print([('#1fb82e', 'You won the battle:')])
            
            # handle level up
            color_print([('', ' - '), ('#fff', '{} levels'.format(monster.earned_levels))])
            character.levelUp(monster.earned_levels)

            # handle treasures
            treasureCount = monster.apply_modifiers('treasure', character, monster.treasures)
            color_print([('', ' - '), ('#fff', '{} treasures'.format(treasureCount))])
            for i in range(treasureCount):
                player.drawCard(self.treasures)

        else:
            self.runAway(monster, player)

    def runAway(self, monster, player):
        character = player.character

        print('\nYou are not strong enough to fight!')
        input('press Enter to roll...')

        roll = self.die.roll()
        roll = character.applyRunAwayBonus(roll)
        roll = monster.apply_modifiers('run-away', character, roll)

        if roll > 4:
            # success
            color_print([('#32a852', 'rolled a {}'.format(roll))])
            print('\nYou escaped but left all treasure behind.')
        else:
            # failure
            color_print([('#cf0000', 'rolled a {}'.format(roll))])
            print('\nThe monster defeated you:')

            # apply bad stuff
            if monster.bad_stuff:
                monster.bad_stuff['action'](character)

            color_print([('', ' - '), ('#fff', 'lose a level')])
            character.levelDown()

    def discardCard(self, card):
        self.discard.addCard(card)
    