# coding=utf8
'''
Модуль для аутентификации пользователей.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import client_dispatcher, user_dispatcher
import dmgame.messages.messages as messages
import dmgame.packets.incoming.auth as incoming
import dmgame.packets.outcoming.auth as outcoming
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
        logger.debug('sending user request message')
        message = messages.UserRequestMessage(user, connection_id, packet)
        user_dispatcher.dispatch(message)
        
    def _on_client_request(self, message):
        '''
        Выполняется при запросе от клиента.
        @param message: ClientRequestMessage
        '''
        connection_id = message.connection_id
        packet = message.packet
        if connection_id in self._authenticated:
            self._send_user_request_message(self._authenticated[connection_id], connection_id, packet)
            
    def _authenticate_user(self, connection_id, packet):
        '''
        Аутентифицирует пользователя.
        @param connection_id: int
        @param packet: IncomingPacket
        '''
        logger.debug('handling auth request')
        user = User(1)
        self._authenticated[connection_id] = user
        response_packet = outcoming.LoginStatusPacket(outcoming.LoginStatusPacket.STATUS_OK)
        message = messages.UserResponseMessage(user, connection_id, response_packet)
        user_dispatcher.dispatch(message)
            
    def _on_client_login_request(self, message):
        '''
        Вызывается при запросе клиента на авторизацию.
        @param Message: LoginMessage
        '''
        self._authenticate_user(message.connection_id, message.packet)
            
    def _send_user_disconnected_message(self, user, connection_id):
        '''
        Рассылает сообщение, что пользователь отключился.
        @param user: User
        @param connection_id: int
        '''
        logger.debug('sending user disconnected message')
        message = messages.UserDisconnectedMessage(user, connection_id)
        user_dispatcher.dispatch(message)
            
    def _on_client_disconnected(self, message):
        '''
        Выполняется при отключении клиента.
        @param message: ClientDisconnectedMessage
        '''
        logger.debug('removing authenticated user')
        connection_id = message.connection_id
        if connection_id in self._authenticated:
            user = self._authenticated[connection_id]
            logger.debug('user %s log out'%user)
            self._send_user_disconnected_message(user, connection_id)
            del self._authenticated[connection_id]
            
    def _on_user_response(self, message):
        '''
        Расссылает сообщение, что есть ответ клиенту.
        @param message: UserResponseMessage
        '''
        logger.debug('sending client response message')
        new_message = messages.ClientResponseMessage(message.connection_id, message.packet)
        client_dispatcher.dispatch(new_message)
        
    def _subscribe(self):
        '''
        Подписывается на всякие сообщения.
        '''
        client_dispatcher.subscribe(messages.ClientRequestMessage, self._on_client_request)
        client_dispatcher.subscribe(messages.ClientDisconnectedMessage, self._on_client_disconnected)
        client_dispatcher.subscribe_for_packet(incoming.LoginPacket, self._on_client_login_request)
        user_dispatcher.subscribe(messages.UserResponseMessage, self._on_user_response)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing auth manager')
        self._subscribe()
