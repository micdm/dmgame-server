# coding=utf8
'''
Игровой стол.
@author: Mic, 2011
'''

from random import choice

from dmgame.db.models.table import GamblingTable
from dmgame.db.models.table_member import TableMember
from dmgame.db.processors.table import GamblingTableProcessor
from dmgame.messages.dispatcher import player_dispatcher 
import dmgame.messages.messages as messages
import dmgame.modules.game.errors as errors
import dmgame.packets.incoming.game as incoming
import dmgame.packets.outcoming.game as outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

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


class TableManager(object):
    '''
    Абстрактный игровой стол.
    '''
    
    RESULT_DEFEAT = 'defeat'
    RESULT_WIN = 'win'

    def __init__(self, model):
        '''
        @param model: GamblingTable
        '''
        self._model = model
        self._set_players_game_flag(True)
        self._subscribe()
        self._start()
        self._save()
    
    @classmethod
    def _get_member_class(cls):
        '''
        Возвращает класс члена игрового стола.
        @return: type
        '''
        return TableMember
    
    @classmethod
    def _get_member_object(cls, number, player):
        '''
        Возвращает объект члена игрового стола.
        @param number: int
        @param player: PLayer
        @return: TableMember
        '''
        member = cls._get_member_class()()
        member.number = number
        member.player = player
        return member
    
    @classmethod
    def _get_members_from_party(cls, party):
        '''
        Выбирает игроков из группы.
        @param party: PlayersParty
        @return: list
        '''
        return [cls._get_member_object(number, player) for number, player in zip(range(len(party)), party)]
    
    @classmethod
    def from_party(cls, party):
        '''
        Создает стол из группы игроков.
        @param party: PlayersParty
        @return: TableManager
        '''
        model = GamblingTable()
        members = cls._get_members_from_party(party)
        model.set_members(members)
        return cls(model)
    
    def _set_players_game_flag(self, value):
        '''
        Выставляет игрокам флажки, что они сейчас играют (или уже не играют).
        @param value: bool
        '''
        for player in self._model.get_players():
            player.is_in_game = value
            
    def _save(self):
        '''
        Сохраняет состояние стола в БД.
        '''
        GamblingTableProcessor.save(self._model)
    
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
        for member in self._model.get_members():
            self._send_to_member(member, packet)
    
    def _send_game_started_packet(self):
        '''
        Рассылает сообщение, что игра началась.
        '''
        members = self._model.get_members()
        for member in members:
            packet = outcoming.GameStartedPacket(member, members)
            self._send_to_member(member, packet)

    def _start(self):
        '''
        Начинает игру.
        '''
        self._send_game_started_packet()
        self._on_start()
        
    def _send_game_ended_packet(self):
        '''
        Рассылает игрокам сообщение, что игра завершилась.
        '''
        packet = outcoming.GameEndedPacket()
        self._send_to_all(packet)
        
    def _send_game_ended_message(self):
        '''
        Рассылает сообщение, что игра завершилась.
        '''
        message = messages.GameEndedMessage(self)
        player_dispatcher.dispatch(message)
    
    def _end(self):
        '''
        Заканчивает игру.
        '''
        self._on_end()
        self._send_game_ended_packet()
        self._unsubscribe()
        self._model.is_ended = True
        self._set_players_game_flag(False)
        self._send_game_ended_message()
        
    def _get_current_turning_member(self):
        '''
        Возвращает игрока, ходящего в данный момент.
        @return: TableMember
        '''
        for member in self._model.get_members():
            if member.is_turning:
                return member
        return None
    
    def _send_member_turning_packet(self, member_turning):
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
        self._send_member_turning_packet(member)
        
    def _set_random_member_turning(self):
        '''
        Делает случайного игрока ходящим.
        '''
        member = choice(self._model.get_members())
        self._set_member_turning(member)
        
    def _set_next_member_turning(self):
        '''
        Передает ход следующему игроку.
        '''
        members = self._model.get_members()
        current = self._get_current_turning_member()
        current_index = members.index(current)
        if current_index == len(members) - 1:
            next = 0
        else:
            next = current_index + 1
        self._set_member_turning(members[next])
        
    def _are_all_results_set(self):
        '''
        Установлены ли результаты для всех игроков?
        @return: bool
        '''
        for member in self._model.get_members():
            if member.result is None:
                return False
        return True
    
    def _send_results_message(self):
        '''
        Рассылает сообщение о результатах.
        '''
        members = self._model.get_members()
        packet = outcoming.ResultsAvailablePacket(members)
        self._send_to_all(packet)

    def _set_member_result(self, member, result):
        '''
        Устанавливает для игрока результат (выиграл/проиграл).
        @param member: TableMember
        @param result: string
        '''
        logger.debug('player %s has now result "%s"'%(member, result))
        member.result = result
        if self._are_all_results_set():
            self._send_results_message()
            self._save()

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
        if self._model.is_ended:
            return
        player = message.player
        if self._model.has_player(player):
            member = self._model.get_member_by_player(player)
            if member.is_turning:
                turn = self._get_turn_object(member, message.packet.data)
                logger.debug('player %s made a turn %s'%(member, turn))
                self._on_member_turn(member, turn)
            else:
                logger.debug('player %s is not turning now'%member)
        
    def _send_member_leaving_packet(self, member_leaving):
        '''
        Рассылает сообщение, что игрок вышел из игры.
        @param member_left: TableMember
        '''
        packet = outcoming.MemberLeavingPacket(member_leaving)
        for member in self._model.get_members():
            if member != member_leaving:
                self._send_to_member(member, packet)

    def _handle_player_leave(self, message):
        '''
        Обрабатывает выход игрока.
        @param message: PlayerDisconnectedMessage
        '''
        player = message.player
        if self._model.has_player(player):
            member = self._model.get_member_by_player(player)
            self._send_member_leaving_packet(member)
            self._on_member_leaving(member)
        
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

    def _on_member_leaving(self, member_leaving):
        '''
        Выполняется, когда игрок уходит.
        @param member: TableMember
        '''
        logger.debug('player %s has left'%member_leaving)
