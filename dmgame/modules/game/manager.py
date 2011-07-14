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

    def _on_game_started(self, message):
        '''
        Вызывается при начале новой игры.
        @param message: GameStartedMessage
        '''
        logger.debug('starting game')
        table = a_la_21.GamblingTable(message.party)
        self._tables.append(table)

    def _subscribe(self):
        '''
        Подписывается на всякие сообщения.
        '''
        player_dispatcher.subscribe(messages.GameStartedMessage, self._on_game_started)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing game manager')
        self._subscribe()
