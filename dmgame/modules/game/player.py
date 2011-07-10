# coding=utf8
'''
Работа с игроками.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import player_dispatcher
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
