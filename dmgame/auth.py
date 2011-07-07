# coding=utf8
'''
Модуль для аутентификации пользователей.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import Dispatcher
from dmgame.messages.messages import ClientRequestMessage, ClientDisconnectedMessage, ServerResponseMessage, UserRequestMessage
from dmgame.packets.incoming.auth import LoginPacket
from dmgame.packets.outcoming.auth import LoginStatusPacket
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
        self.id = id
        
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return '#%s'%self.id


class AuthManager(object):
    '''
    Менеджер аутентификации.
    '''

    def __init__(self):
        self._authenticated = {}
        
    def _send_user_request_message(self, user, connection_id, packet):
        '''
        Отправляет сообщение от авторизованного пользователя.
        @param user: User
        @param connection_id: int
        @param packet: IncomingPacket
        '''
        logger.debug('dispatching user request message')
        message = UserRequestMessage(user, connection_id, packet)
        Dispatcher.dispatch(message)
        
    def _authenticate_user(self, connection_id, packet):
        '''
        Аутентифицирует пользователя.
        @param connection_id: int
        @param packet: IncomingPacket
        '''
        logger.debug('handling auth request')
        self._authenticated[connection_id] = User(1)
        response_packet = LoginStatusPacket(LoginStatusPacket.STATUS_OK)
        message = ServerResponseMessage(connection_id, response_packet)
        Dispatcher.dispatch(message)
    
    def _on_client_request(self, message):
        '''
        Выполняется при запросе от клиента.
        @param message: dmgame.messages.messages.ClientRequestMessage
        '''
        connection_id = message.connection_id
        packet = message.packet
        if isinstance(packet, LoginPacket):
            self._authenticate_user(connection_id, packet)
        if connection_id in self._authenticated:
            self._send_user_request_message(self._authenticated[connection_id], connection_id, packet)
            
    def _on_client_disconnected(self, message):
        '''
        Выполняется при отключении клиента.
        @param message: dmgame.messages.messages.ClientDisconnectedMessage
        '''
        logger.debug('removing authenticated user')
        connection_id = message.connection_id
        if connection_id in self._authenticated:
            user = self._authenticated[connection_id]
            logger.debug('user %s log out'%user)
            del self._authenticated[connection_id]

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing auth manager')
        Dispatcher.subscribe(ClientRequestMessage, self._on_client_request)
        Dispatcher.subscribe(ClientDisconnectedMessage, self._on_client_disconnected)
