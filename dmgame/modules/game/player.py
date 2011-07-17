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


class PlayersParty(list):
    '''
    Компания игроков.
    '''
    
    # Время до роспуска после сформирования (в секундах):
    DISMISS_TIME = 5

    def __init__(self, players):
        '''
        @param players: list
        '''
        super(PlayersParty, self).__init__()
        self.extend(players)
        self._ready = []
        self._timer = None
        self._set_players_party_flag(True)
        self._subscribe()
        self._start_timer()

    def __str__(self):
        return '<party of %s>'%len(self)
    
    def _deinit(self):
        '''
        Деинициализирует группу.
        '''
        self._unsubscribe()
        self._stop_timer()
        self._set_players_party_flag(False)
        
    def _set_players_party_flag(self, value):
        '''
        Выставляет игрокам флажки, что они сейчас в группе (либо уже нет).
        @param value: bool
        '''
        for player in self:
            player.is_in_party = value

    def _send_dismiss_message_to_players(self):
        '''
        Рассылает участникам сообщение о роспуске группы.
        '''
        for player in self:
            packet = outcoming.PartyDismissPacket()
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)
            
    def _send_dismiss_message(self):
        '''
        Рассылает сообщение о роспуске группы.
        '''
        message = messages.PartyDismissedMessage(self)
        player_dispatcher.dispatch(message)
    
    def _dismiss(self):
        '''
        Распускает группу.
        '''
        logger.debug('dismissing party')
        self._send_dismiss_message_to_players()
        self._send_dismiss_message()
        self._deinit()

    def _on_player_accepted(self, message):
        '''
        Выполняется при подтверждении пользователем готовности играть.
        @param message: AcceptInvitePacket
        '''
        player = message.player
        if player not in self._ready:
            self._ready.append(player)
        for player in self:
            packet = outcoming.PartyMemberReadyPacket(self, self._ready)
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)
        if len(self._ready) == len(self):
            self._deinit()
            message = messages.PartyReadyMessage(self)
            player_dispatcher.dispatch(message)
            
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
        player_dispatcher.subscribe_for_packet(incoming.AcceptInvitePacket, self._on_player_accepted, self)
        player_dispatcher.subscribe(messages.PlayerDisconnectedMessage, self._on_player_disconnected, self)
        
    def _unsubscribe(self):
        '''
        Отписывается от сообщений.
        '''
        player_dispatcher.unsubscribe_from_all(self)
        
    def _start_timer(self):
        '''
        Запускает таймер, по истечении которого группа будет распущена.
        '''
        logger.debug('starting party timer for %s seconds'%self.DISMISS_TIME)
        self._timer = Timer(self.DISMISS_TIME, self._dismiss)
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
        for player in self:
            packet = outcoming.PartyInvitePacket(self.DISMISS_TIME)
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)
