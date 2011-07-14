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
import dmgame.packets.outcoming.game as outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class TableMember(object):
    '''
    Член игрового стола.
    '''
    
    def __init__(self, number, player):
        '''
        @param number: int
        @param player: Player
        '''
        self.number = number
        self.player = player
        self.is_turning = False
        self.is_turning_first = False
        self.result = None
        
    def __str__(self):
        return str(self.player)
    
    def __eq__(self, other):
        return self.player == other.player
    
    def __ne__(self, other):
        return not self.__eq__(other)


class PlayerTurn(object):
    '''
    Ход игрока.
    '''

    def __init__(self, member, turn_data):
        '''
        @param member: TableMember
        @param turn_data: dict
        '''
        self.member = member
        self._handle_turn_data(turn_data)
        self._check()
        
    def __str__(self):
        return '<%s>'%type(self).__name__
    
    def _handle_turn_data(self, turn_data):
        '''
        Заполняет объект из входящих данных.
        @param turn_data: dict
        '''
    
    def _check(self):
        '''
        Проверяет полученный объект.
        '''
        
        
class GameResults(object):
    '''
    Результаты игры.
    '''

    RESULT_DEFEAT = 'defeat'
    RESULT_WIN = 'win'

    def __init__(self, members):
        '''
        @param members: dict
        '''
        self._members = members
        
    def _are_all_results_set(self):
        '''
        Установлены ли результаты для всех игроков?
        @return: bool
        '''
        for member in self._members.values():
            if member.result is None:
                return False
        return True
    
    def _send_results_message(self):
        '''
        Рассылает сообщение о результатах.
        '''
        members = self._members.values()
        packet = outcoming.ResultsAvailablePacket(members)
        for member in members:
            message = messages.PlayerResponseMessage(member.player, packet)
            player_dispatcher.dispatch(message)

    def set_member_result(self, member, result):
        '''
        Устанавливает для игрока результат (выиграл/проиграл).
        @param member: TableMember
        @param result: string
        '''
        logger.debug('player %s has now result "%s"'%(member, result))
        member.result = result
        if self._are_all_results_set():
            self._send_results_message()


class GamblingTable(object):
    '''
    Абстрактный игровой стол.
    '''

    def __init__(self, party):
        '''
        @param party: PlayersParty
        '''
        self._members = self._get_table_members(party)
        self._results = GameResults(self._members)
        self._is_ended = False
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
        for number, player in zip(range(len(party)), party):
            members[player] = member_class(number, player)
        return members
    
    def _send_to_member(self, member, packet):
        '''
        Отправляет сообщение конкретному игроку.
        @param member: TableMember
        @param packet: OutcomingPacket
        '''
        message = messages.PlayerResponseMessage(member.player, packet)
        player_dispatcher.dispatch(message)
        
    def _send_to_all(self, packet):
        '''
        Рассылает сообщение всем.
        @param packet: OutcomingPacket
        '''
        for member in self._members.values():
            self._send_to_member(member, packet)
    
    def _send_game_started_message(self):
        '''
        Рассылает сообщение, что игра началась.
        '''
        members = self._members.values()
        for member in members:
            packet = outcoming.GameStartedPacket(member, members)
            self._send_to_member(member, packet)

    def _start(self):
        '''
        Начинает игру.
        '''
        self._send_game_started_message()
        self._on_start()
    
    def _end(self):
        '''
        Заканчивает игру.
        '''
        self._is_ended = True
        self._unsubscribe()
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
    
    def _send_member_turning_message(self, member_turning):
        '''
        Рассылает сообщение, что игрок теперь ходит.
        @param member_turning: TableMember
        '''
        packet = outcoming.MemberTurningPacket(member_turning)
        self._send_to_all(packet)
    
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
        self._send_member_turning_message(member)
        
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
        members = self._members.values()
        current = self._get_current_turning_member()
        current_index = members.index(current)
        if current_index == len(members) - 1:
            next = 0
        else:
            next = current_index + 1
        self._set_member_turning(members[next])

    def _get_turn_class(self, turn_type):
        '''
        Возвращает класс хода.
        @param turn_type: string
        @return: PlayerTurn
        '''
        raise NotImplementedError()
    
    def _get_turn_object(self, member, turn_data):
        '''
        Возвращает объект хода.
        @param member: TableMember
        @param turn_data: dict
        @return: PlayerTurn
        '''
        if 'type' not in turn_data:
            raise errors.BadTurnDataError('turn data must contain "type" field')
        turn_type = turn_data['type']
        turn_class = self._get_turn_class(turn_type)
        if turn_class is None:
            raise errors.BadTurnDataError('unknown turn type "%s"'%turn_type)
        return turn_class(member, turn_data)

    def _handle_player_turn(self, message):
        '''
        Обрабатывает ход игрока.
        @param message: PlayerRequestMessage
        '''
        if self._is_ended:
            return
        player = message.player
        if player not in self._members:
            logger.debug('player %s not in members, skipping'%player)
            return
        member = self._members[player]
        if not member.is_turning:
            logger.debug('player %s is not turning now'%member)
            return
        turn = self._get_turn_object(member, message.packet.data)
        logger.debug('player %s made a turn %s'%(member, turn))
        self._on_member_turn(member, turn)

    def _handle_player_leave(self, message):
        '''
        Обрабатывает выход игрока.
        @param message: PlayerDisconnectedMessage
        '''
        player = message.player
        if player in self._members:
            self._on_member_leave(self._members[player])
        
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
