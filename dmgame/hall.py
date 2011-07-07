# coding=utf8
'''
Модуль для игрового зала.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import player_dispatcher, user_dispatcher
import dmgame.messages.messages as messages
import dmgame.packets.incoming.hall as incoming
import dmgame.packets.outcoming.hall as outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)
from dmgame.utils.timer import Timer

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
        self._ready = []
        self._timer = None
        self._subscribe()
        self._start_timer()

    def __str__(self):
        return '<party of %s>'%len(self.players)
    
    def _send_dismiss_message_to_players(self):
        '''
        Рассылает участникам сообщение о роспуске группы.
        '''
        for player in self.players:
            packet = outcoming.PartyDismissPacket()
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)
            
    def _send_dismiss_message(self):
        '''
        Рассылает сообщение о роспуске группы.
        '''
        message = messages.PartyDismissMessage(self)
        player_dispatcher.dispatch(message)
    
    def _dismiss(self):
        '''
        Распускает группу.
        '''
        logger.debug('dismissing party')
        self._unsubscribe()
        self._stop_timer()
        self._send_dismiss_message_to_players()
        self._send_dismiss_message()
    
    def _on_player_accepted(self, message):
        '''
        Выполняется при подтверждении пользователем готовности играть.
        @param message: AcceptInvitePacket
        '''
        player = message.player
        if player not in self._ready:
            self._ready.append(player)
        for player in self.players:
            packet = outcoming.PartyMemberReadyPacket(self.players, self._ready)
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)
        if len(self._ready) == len(self.players):
            self._stop_timer()
            logger.debug('starting game')
            
    def _on_player_disconnected(self, message):
        '''
        Выполняется при отключении игрока.
        @param message: PlayerDisconnectedMessage
        '''
        self._dismiss()
    
    def _subscribe(self):
        '''
        Подписывается на нужные сообщения.
        '''
        player_dispatcher.subscribe_for_packet(incoming.AcceptInvitePacket, self._on_player_accepted)
        player_dispatcher.subscribe(messages.PlayerDisconnectedMessage, self._on_player_disconnected)
        
    def _unsubscribe(self):
        '''
        Отписывается от сообщений.
        '''
        player_dispatcher.unsubscribe_from_packet(incoming.AcceptInvitePacket, self._on_player_accepted)
        player_dispatcher.unsubscribe(messages.PlayerDisconnectedMessage, self._on_player_disconnected)
        
    def _start_timer(self):
        '''
        Запускает таймер, по истечении которого группа будет распущена.
        '''
        logger.debug('starting party timer')
        self._timer = Timer(5, self._dismiss)
        self._timer.start()
        
    def _stop_timer(self):
        '''
        Останавливает таймер.
        '''
        if self._timer:
            logger.debug('stopping party timer')
            self._timer.stop()
            self._timer = None
        else:
            logger.debug('party timer already stopped')
    
    def invite(self):
        '''
        Рассылает приглашения игрокам начать игру.
        '''
        for player in self.players:
            packet = outcoming.PartyInvitePacket()
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)


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

    def _on_user_request(self, message):
        '''
        Рассылает сообщение, что от игрока получен запрос.
        @param message: UserRequestMessage
        '''
        logger.debug('sending player request message')
        player = Player(message.user, message.connection_id)
        new_message = messages.PlayerRequestMessage(player, message.packet)
        player_dispatcher.dispatch(new_message)
        
    def _on_user_disconnected(self, message):
        '''
        Рассылает сообщение, что игрок отключился.
        @param message: UserDisconnectedMessage
        '''
        logger.debug('sending player disconnected message')
        player = Player(message.user, message.connection_id)
        new_message = messages.PlayerDisconnectedMessage(player)
        player_dispatcher.dispatch(new_message)
        
    def _on_player_response(self, message):
        '''
        Рассылает сообщение, что пользователь получает ответ.
        @param message: PlayerResponseMessage
        '''
        logger.debug('sending user response message')
        player = message.player
        new_message = messages.UserResponseMessage(player.user, player.connection_id, message.packet)
        user_dispatcher.dispatch(new_message)

    def _on_player_enter_request(self, message):
        '''
        Выполняется при запросе пользователя на вход в зал.
        @param message: EnterPacket
        '''
        logger.debug('handling hall enter request')
        packet = outcoming.WelcomePacket()
        message = messages.PlayerResponseMessage(message.player, packet)
        player_dispatcher.dispatch(message)
        
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
            party.invite()

    def _on_player_play_request(self, message):
        '''
        Выполняется при запросе пользователя на игру.
        @param message: PlayPacket
        '''
        logger.debug('handling hall play request')
        self._add_to_queue(message.player)
        
    def _subscribe(self):
        '''
        Подписывается на всякие сообщения.
        '''
        user_dispatcher.subscribe(messages.UserRequestMessage, self._on_user_request)
        user_dispatcher.subscribe(messages.UserDisconnectedMessage, self._on_user_disconnected)
        player_dispatcher.subscribe(messages.PlayerResponseMessage, self._on_player_response)
        player_dispatcher.subscribe_for_packet(incoming.EnterPacket, self._on_player_enter_request)
        player_dispatcher.subscribe_for_packet(incoming.PlayPacket, self._on_player_play_request)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing hall manager')
        self._subscribe()
