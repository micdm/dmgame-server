# coding=utf8
'''
Инициализация сервера.
@author: Mic, 2011
'''

from dmgame import settings
from dmgame.modules.auth.manager import AuthManager
from dmgame.modules.hall.manager import HallManager
from dmgame.servers.ws.server import Server
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

def init():
    '''
    Инициализирует все основные модули.
    '''
    logger.info('initializing')
    AuthManager().init()
    HallManager().init()
    Server(settings.SERVERS['ws']).init()
    logger.info('deinitializing')
