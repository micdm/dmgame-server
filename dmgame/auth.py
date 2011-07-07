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
    
    
class MessageResender(object):
    '''
    Пересыльщик сообщений на новый уровень - от транспорта к пользователю.
    '''
    
    def __init__(self, authenticated):
        '''
        @param authenticated: dict
        '''
        self._authenticated = authenticated
        self._subscribe()

    def _on_client_request(self, message):
        '''
        Выполняется при запросе от клиента.
        @param message: ClientRequestMessage
        '''
        connection_id = message.connection_id
        if connection_id in self._authenticated:
            user = self._authenticated[connection_id]
            new_message = messages.UserRequestMessage(user, connection_id, message.packet)
            user_dispatcher.dispatch(new_message)
            
    def _on_client_disconnected(self, message):
        '''
        Выполняется при отключении клиента.
        @param message: ClientDisconnectedMessage
        '''
        connection_id = message.connection_id
        if connection_id in self._authenticated:
            user = self._authenticated[connection_id]
            logger.debug('user %s log out'%user)
            new_message = messages.UserDisconnectedMessage(user, connection_id)
            user_dispatcher.dispatch(new_message)
            
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
        Подписывается на сообщения.
        '''
        client_dispatcher.subscribe(messages.ClientRequestMessage, self._on_client_request)
        client_dispatcher.subscribe(messages.ClientDisconnectedMessage, self._on_client_disconnected)
        user_dispatcher.subscribe(messages.UserResponseMessage, self._on_user_response)


class AuthManager(object):
    '''
    Менеджер аутентификации.
    '''

    def __init__(self):
        self._authenticated = {}
        self._message_resender = MessageResender(self._authenticated)
        
    def _authenticate(self, connection_id, packet):
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
        self._authenticate(message.connection_id, message.packet)
        
    def _on_user_disconnected(self, message):
        '''
        Выполняется при отключении пользователя.
        @param message: UserDisconnectedMessage
        '''
        logger.debug('removing authenticated user')
        connection_id = message.connection_id
        if connection_id in self._authenticated:
            del self._authenticated

    def _subscribe(self):
        '''
        Подписывается на всякие сообщения.
        '''
        client_dispatcher.subscribe_for_packet(incoming.LoginPacket, self._on_client_login_request)
        user_dispatcher.subscribe(messages.UserDisconnectedMessage, self._on_user_disconnected)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing auth manager')
        self._subscribe()
