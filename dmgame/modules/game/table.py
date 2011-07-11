# coding=utf8
'''
Игровой стол.
@author: Mic, 2011
'''

from random import choice

from dmgame.messages.dispatcher import player_dispatcher 
import dmgame.messages.messages as messages
import dmgame.modules.game.errors as errors
import dmgame.packets.incoming.game as incoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class PlayerTurn(object):
    '''
    Ход игрока.
    '''

    def __init__(self, player, turn_data):
        '''
        @param player: Player
        @param turn_data: dict
        '''
        self.player = player
        self._handle_turn_data(turn_data)
        self._check()
    
    def _handle_turn_data(self, turn_data):
        '''
        Заполняет объект из входящих данных.
        @param turn_data: dict
        '''
    
    def _check(self):
        '''
        Проверяет полученный объект.
        '''


class GamblingTable(object):
    '''
    Абстрактный игровой стол.
    '''
    
    PLAYER_RESULT_DEFEAT = 0
    PLAYER_RESULT_WIN = 1

    def __init__(self, party):
        '''
        @param party: PlayersParty
        '''
        self._party = party
        self._first_turning_player = None
        self._turning_player = None
        self._subscribe()
        self._start()

    def _start(self):
        '''
        Начинает игру.
        '''
        self._on_start()
    
    def _end(self):
        '''
        Заканчивает игру.
        '''
        self._on_end()
    
    def _set_player_turning(self, player):
        '''
        Делает игрока ходящим.
        @param player: Player
        '''
        logger.debug('player %s turning now'%player)
        if self._first_turning_player is None:
            self._first_turning_player = player
        self._turning_player = player
        
    def _set_random_player_turning(self):
        '''
        Делает случайного игрока ходящим.
        '''
        player = choice(self._party.players)
        self._set_player_turning(player)
        
    def _set_next_player_turning(self):
        '''
        Передает ход следующему игроку.
        '''
        players = self._party.players
        current = players.index(self._turning_player)
        if current == len(players) - 1:
            next = 0
        else:
            next = current + 1
        self._set_next_player_turning(players[next])
    
    def _set_player_result(self, player, result):
        '''
        Устанавливает для игрока результат (выиграл/проиграл).
        @param player: Player
        '''
        logger.debug('player %s has now result %s'%(player, result))
        
    def _get_turn_object(self, turn_data):
        '''
        Возвращает объект хода.
        @param turn_data: dict
        @return: PlayerTurn
        '''
        raise NotImplementedError()

    def _handle_player_turn(self, message):
        '''
        Обрабатывает ход игрока.
        @param message: PlayerRequestMessage
        '''
        player = message.player
        if player == self._turning_player:
            turn = self._get_turn_object(message.turn)
            self._on_player_turn(player, turn)
            
    def _handle_player_leave(self, message):
        '''
        Обрабатывает выход игрока.
        @param message: PlayerDisconnectedMessage
        '''
        self._on_player_leave(message.player)
        
    def _subscribe(self):
        '''
        Подписывается на разные события.
        '''
        player_dispatcher.subscribe_for_packet(incoming.PlayerTurnPacket, self._handle_player_turn, self)
        player_dispatcher.subscribe(messages.PlayerDisconnectedMessage, self._handle_player_leave, self)
        
    def _unsubscribe(self):
        '''
        Отписывается от событий.
        '''
        player_dispatcher.unsubscribe_from_all(self)
        
    def _on_start(self):
        '''
        Вызывается при старте игры.
        Можно использовать в наследующих классах как место для первичной инициализации.
        '''
        logger.debug('starting game')
        
    def _on_end(self):
        '''
        Вызывается при окончании игры.
        '''
        
    def _on_player_turn(self, player, turn):
        '''
        Выполняется, когда игрок ходит.
        @param player: Player
        @param turn: dict
        '''
        logger.debug('player %s has made a turn %s'%(player, turn))

    def _on_player_leave(self, leaver):
        '''
        Выполняется, когда игрок уходит.
        @param leaver: Player
        '''
        logger.debug('player %s has left'%leaver)
