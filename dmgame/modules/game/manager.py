# coding=utf8
'''
Менджер игр.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import player_dispatcher 
import dmgame.messages.messages as messages
from dmgame.modules.game.table import GamblingTable
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class GameManager(object):
    '''
    Упраление игровыми столами.
    '''

    def __init__(self):
        self._tables = []

    def _on_game_started(self, message):
        '''
        Вызывается при начале новой игры.
        @param message: GameStartedMessage
        '''
        logger.debug('starting game')
        table = GamblingTable(message.party)
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
