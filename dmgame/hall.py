# coding=utf8
'''
Модуль для игрового зала.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import Dispatcher
from dmgame.messages.messages import ServerResponseMessage, UserRequestMessage
import dmgame.packets.incoming.hall as incoming
import dmgame.packets.outcoming.hall as outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Player(object):
    '''
    Игрок. Один зарегистрированный пользователь может играть из нескольких мест,
    поэтому игрок - это пользователь плюс конкретное соединение.
    '''
    
    def __init__(self, user, connection_id):
        '''
        @param user: User
        @param connection_id: int
        '''
        self.user = user
        self.connection_id = connection_id
        
    def __eq__(self, other):
        return self.user == other.user and self.connection_id == other.connection_id

    def __ne__(self, other):
        return not self.__eq__(other)


class PlayersParty(object):
    '''
    Компания игроков.
    '''

    def __init__(self, players):
        '''
        @param players: list
        '''
        self.players = players
        self._subscribe()

    def __str__(self):
        return '<party of %s>'%len(self.players)
    
    def _subscribe(self):
        '''
        Подписывается на нужные сообщения.
        '''
        
    
    def invite_players(self):
        '''
        Рассылает приглашения игрокам начать игру.
        '''
        for player in self.players:
            packet = outcoming.PartyInvitePacket()
            message = ServerResponseMessage(player.connection_id, packet)
            Dispatcher.dispatch(message)


class PlayersQueue(object):
    '''
    Очередь игроков.
    '''
    
    PARTY_SIZE = 2
    
    def __init__(self):
        self._queue = []
        
    def has_player(self, player):
        '''
        Возвращает, есть ли игрок в очереди.
        @param player: Player
        @return: bool
        '''
        return player in self._queue
    
    def add_player(self, player):
        '''
        Добавляет в очередь игрока.
        @param player: Player
        '''
        self._queue.append(player)
        
    def remove_party(self, party):
        '''
        Удаляет из очереди игроков группы.
        @param party: PlayersParty
        '''
        for player in party.players:
            self._queue.remove(player)
        
    def find_party_for_last_player(self):
        '''
        Находит компанию для последнего игрока в очереди.
        @return: PlayersParty
        '''
        last = self._queue[-1]
        if len(self._queue) >= self.PARTY_SIZE:
            count = self.PARTY_SIZE - 1
            return PlayersParty(self._queue[:count] + [last])
        return None


class HallManager(object):
    '''
    Игровой зал.
    '''

    def __init__(self):
        self._players_queue = PlayersQueue()

    def _send_welcome_to_hall(self, connection_id):
        '''
        Отправляет приветствие вошедшему в игровой зал.
        @param connection_id: int
        '''
        logger.debug('handling hall request')
        packet = outcoming.WelcomePacket()
        message = ServerResponseMessage(connection_id, packet)
        Dispatcher.dispatch(message)
        
    def _add_to_queue(self, player):
        '''
        Добавляет игрока в очередь.
        @param player: Player
        '''
        if self._players_queue.has_player(player):
            logger.debug('player already in queue')
            return
        logger.debug('adding to players queue')
        self._players_queue.add_player(player)
        party = self._players_queue.find_party_for_last_player()
        if party is None:
            logger.debug('no party yet')
        else:
            logger.debug('party %s found, removing party from queue and sending invites'%party)
            self._players_queue.remove_party(party)
            party.invite_players()
        
    def _on_user_enter_request(self, message):
        '''
        Выполняется при запросе пользователя на вход в зал.
        @param message: EnterMessage
        '''
        self._send_welcome_to_hall(message.connection_id)

    def _on_user_play_request(self, message):
        '''
        Выполняется при запросе пользователя на игру.
        @param message: PlayPacket
        '''
        player = Player(message.user, message.connection_id)
        self._add_to_queue(player)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing hall manager')
        Dispatcher.subscribe_for_user_request(incoming.EnterPacket, self._on_user_enter_request)
        Dispatcher.subscribe_for_user_request(incoming.PlayPacket, self._on_user_play_request)
