# coding=utf8
'''
Модуль для аутентификации пользователей.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import Dispatcher
from dmgame.messages.messages import ClientRequestMessage, ClientDisconnectedMessage, ServerResponseMessage, UserRequestMessage
from dmgame.servers.ws.packets import incoming, outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class User(object):
    '''
    Класс пользователя.
    '''
    
    def __init__(self, id):
        '''
        @param id: int
        '''
        self._id = id
        
    def __str__(self):
        return 'user #%s'%self._id


class AuthManager(object):
    '''
    Менеджер аутентификации.
    '''

    def __init__(self):
        self._authenticated = {}
        
    def _dispatch_user_request_message(self, user, handler_id, packet):
        '''
        Отправляет сообщение от авторизованного пользователя.
        @param user: User
        @param handler_id: int
        @param packet: IncomingPacket
        '''
        logger.debug('handler authenticated, dispatching user request message')
        message = UserRequestMessage(user, handler_id, packet)
        Dispatcher.dispatch(message)
        
    def _authenticate_user(self, handler_id, packet):
        '''
        Аутентифицирует пользователя.
        @param handler_id: int
        @param packet: IncomingPacket
        '''
        logger.debug('handling auth request')
        self._authenticated[handler_id] = User(1)
        response_packet = outcoming.AuthPacket(outcoming.AuthPacket.STATUS_OK)
        message = ServerResponseMessage(handler_id, response_packet)
        Dispatcher.dispatch(message)
    
    def _on_client_request(self, message):
        '''
        Выполняется при запросе от клиента.
        @param message: dmgame.messages.messages.ClientRequestMessage
        '''
        handler_id = message.handler_id
        packet = message.packet
        if isinstance(packet, incoming.AuthPacket):
            self._authenticate_user(handler_id, packet)
        if handler_id in self._authenticated:
            self._dispatch_user_request_message(self._authenticated[handler_id], handler_id, packet)
            
    def _on_client_disconnected(self, message):
        '''
        Выполняется при отключении клиента.
        @param message: dmgame.messages.messages.ClientDisconnectedMessage
        '''
        logger.debug('removing authenticated user')
        handler_id = message.handler_id
        if handler_id in self._authenticated:
            user = self._authenticated[handler_id]
            logger.debug('user %s log out'%user)
            del self._authenticated[handler_id]

    def init(self):
        '''
        Инициализация.
        '''
        logger.debug('initializing auth manager')
        Dispatcher.subscribe(ClientRequestMessage, self._on_client_request)
        Dispatcher.subscribe(ClientDisconnectedMessage, self._on_client_disconnected)
