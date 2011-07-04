# coding=utf8
'''
Модуль для аутентификации пользователей.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import Dispatcher
from dmgame.messages.messages import ClientRequestMessage, ClientDisconnectedMessage, ServerResponseMessage
from dmgame.servers.ws.packets import incoming, outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class AuthManager(object):
    '''
    Менеджер аутентификации.
    '''
    
    def _on_auth_request(self, message):
        '''
        Выполняется при запросе на аутентификацию.
        @param message: dmgame.messages.messages.ClientRequestMessage
        '''
        packet = message.packet
        if isinstance(packet, incoming.AuthPacket):
            logger.debug('handling auth request')
            packet = outcoming.AuthPacket(outcoming.AuthPacket.STATUS_OK)
            message = ServerResponseMessage(message.handler_id, packet)
            Dispatcher.dispatch(message)
            
    def _on_client_disconnected(self, message):
        '''
        Выполняется при отключении клиента.
        @param message: dmgame.messages.messages.ClientDisconnectedMessage
        '''
        logger.debug('here will be code removing authenticated user')
    
    def init(self):
        '''
        Инициализация.
        '''
        logger.debug('initializing auth manager')
        Dispatcher.subscribe(ClientRequestMessage, self._on_auth_request)
        Dispatcher.subscribe(ClientDisconnectedMessage, self._on_client_disconnected)
