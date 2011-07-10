# coding=utf8
'''
Игровой стол.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import player_dispatcher 
import dmgame.messages.messages as messages
import dmgame.packets.incoming.game as incoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class GamblingTable(object):
    '''
    Абстрактный игровой стол.
    '''

    def __init__(self, party):
        '''
        @param party: PlayersParty
        '''
        self._party = party
        self._subscribe()
        self._on_start()
        
    def _on_player_turn(self, player, turn):
        '''
        Выполняется, когда игрок ходит.
        @param player: Player
        @param turn: dict
        '''
        logger.debug('player %s has made turn %s'%(player, turn))

    def _on_player_disconnected(self, player):
        '''
        Выполняется при отключении игрока.
        @param player: Player
        '''
        logger.debug('player %s disconnected'%player)
        
    def _subscribe(self):
        '''
        Подписывается на разные события.
        '''
        player_dispatcher.subscribe_for_packet(incoming.PlayerTurnPacket,
                                               lambda message: self._on_player_turn(message.player, message.packet.data), self)
        player_dispatcher.subscribe(messages.PlayerDisconnectedMessage,
                                    lambda message: self._on_player_disconnected(message.player), self)
        
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
