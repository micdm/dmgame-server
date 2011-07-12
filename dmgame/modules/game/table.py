# coding=utf8
'''
Игровой стол.
@author: Mic, 2011
'''

from random import choice

from dmgame.messages.dispatcher import player_dispatcher 
import dmgame.messages.messages as messages
import dmgame.packets.incoming.game as incoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class TableMember(object):
    '''
    Член игрового стола.
    '''
    
    def __init__(self, player):
        '''
        @param player: Player
        '''
        self.player = player
        self.is_turning = False
        self.is_turning_first = False
        
    def __str__(self):
        return str(self.player)


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
        self._members = self._get_table_members(party)
        self._subscribe()
        self._start()
        
    def _get_member_class(self):
        '''
        Возвращает класс члена игрового стола.
        @return: TableMember
        '''
        return TableMember
    
    def _get_table_members(self, party):
        '''
        Выбирает игроков из группы.
        @param party: PlayersParty
        @return: dict
        '''
        member_class = self._get_member_class()
        members = {}
        for player in party.players:
            members[player] = member_class(player)
        return members

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
        
    def _get_current_turning_member(self):
        '''
        Возвращает игрока, ходящего в данный момент.
        @return: TableMember
        '''
        for member in self._members.values():
            if member.is_turning:
                return member
        return None
    
    def _set_member_turning(self, member):
        '''
        Делает игрока ходящим.
        @param member: TableMember
        '''
        logger.debug('member %s turning now'%member)
        current = self._get_current_turning_member()
        if current is None:
            member.is_turning_first = True
        else:
            current.is_turning = False
        member.is_turning = True
        
    def _set_random_member_turning(self):
        '''
        Делает случайного игрока ходящим.
        '''
        member = choice(self._members.values())
        self._set_member_turning(member)
        
    def _set_next_member_turning(self):
        '''
        Передает ход следующему игроку.
        '''
        members = self._members
        current = self._get_current_turning_member()
        current_index = members.index(current)
        if current_index == len(members) - 1:
            next = 0
        else:
            next = current_index + 1
        self._set_next_member_turning(members[next])
    
    def _set_member_result(self, member, result):
        '''
        Устанавливает для игрока результат (выиграл/проиграл).
        @param member: TableMember
        '''
        logger.debug('player %s has now result %s'%(member, result))
        
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
        if player in self._members:
            member = self._members[player]
            if member.is_turning:
                turn = self._get_turn_object(message.turn)
                self._on_member_turn(member, turn)
            
    def _handle_player_leave(self, message):
        '''
        Обрабатывает выход игрока.
        @param message: PlayerDisconnectedMessage
        '''
        player = message.player
        if player in self._members:
            self._on_player_leave(self._members[player])
        
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
        
    def _on_member_turn(self, member, turn):
        '''
        Выполняется, когда игрок ходит.
        @param member: TableMember
        @param turn: dict
        '''
        logger.debug('player %s has made a turn %s'%(member, turn))

    def _on_member_leave(self, member):
        '''
        Выполняется, когда игрок уходит.
        @param member: TableMember
        '''
        logger.debug('player %s has left'%member)
