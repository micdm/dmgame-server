# coding=utf8
'''
Модуль для аутентификации пользователей.
@author: Mic, 2011
'''

from dmgame.messages import incoming, outcoming
from dmgame.messages.dispatcher import Dispatcher
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class AuthManager(object):
    '''
    Менеджер аутентификации.
    '''
    
    def _on_auth_request(self, message):
        '''
        Выполняется при запросе на аутентификацию.
        @param message: dmgame.messages.incoming.AuthMessage
        '''
        logger.debug('handling auth request')
        result = outcoming.AuthMessage(outcoming.AuthMessage.STATUS_OK)
        outcoming.create_reply(message, result)
        Dispatcher.dispatch(result)
    
    def init(self):
        '''
        Инициализация.
        '''
        logger.debug('initializing auth manager')
        Dispatcher.subscribe(incoming.AuthMessage, self._on_auth_request)
