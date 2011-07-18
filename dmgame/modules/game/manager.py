# coding=utf8
'''
Менджер игр.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import player_dispatcher 
import dmgame.messages.messages as messages
import dmgame.games.a_la_21.table as a_la_21
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class GameManager(object):
    '''
    Управление игровыми столами.
    '''

    def __init__(self):
        self._tables = []

    def _on_party_ready(self, message):
        '''
        Выполняется, когда группа готова.
        @param message: PartyReadyMessage
        '''
        logger.debug('starting game')
        table = a_la_21.GameTableManager.from_party(message.party)
        self._tables.append(table)
        
    def _on_game_ended(self, message):
        '''
        Выполняется при завершении игры.
        @param message: GameEndedMessage
        '''
        table = message.table
        if table in self._tables:
            self._tables.remove(table)
        logger.debug('game has ended')

    def _subscribe(self):
        '''
        Подписывается на всякие сообщения.
        '''
        player_dispatcher.subscribe(messages.PartyReadyMessage, self._on_party_ready)
        player_dispatcher.subscribe(messages.GameEndedMessage, self._on_game_ended)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing game manager')
        self._subscribe()
