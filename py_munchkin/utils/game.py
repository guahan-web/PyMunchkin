from py_munchkin.utils.eventbus import EventBus
from py_munchkin.utils.monster import Monster
from py_munchkin.utils.door_deck import generateDoorDeck

class Game:
    def __init__(self, max_players = 4):
        self.events = EventBus()
        self.players = []
        self.current_player = None
        self.max_players = max_players
        self.doors = generateDoorDeck()
        

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

    