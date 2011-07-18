# coding=utf8
'''
Менеджер аутентификации пользователей.
@author: Mic, 2011
'''

from dmgame.db.processors.user import UserProcessor
from dmgame.messages.dispatcher import client_dispatcher, user_dispatcher
import dmgame.messages.messages as messages
import dmgame.packets.incoming.auth as incoming
import dmgame.packets.outcoming.auth as outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)
    
    
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
        
    def _authenticate(self, connection_id, login, password):
        '''
        Аутентифицирует пользователя.
        @param connection_id: int
        @param login: string
        @param password: string
        '''
        user = UserProcessor.get_by_login_and_password(login, password)
        if user is None:
            logger.debug('user with login "%s" not found'%login)
            status = outcoming.LoginStatusPacket.STATUS_NOT_FOUND
        else:
            logger.debug('user %s successfully authenticated'%user)
            self._authenticated[connection_id] = user
            status = outcoming.LoginStatusPacket.STATUS_OK
        packet = outcoming.LoginStatusPacket(status)
        message = messages.UserResponseMessage(user, connection_id, packet)
        user_dispatcher.dispatch(message)

    def _on_client_login_request(self, message):
        '''
        Вызывается при запросе клиента на авторизацию.
        @param Message: LoginMessage
        '''
        packet = message.packet
        self._authenticate(message.connection_id, packet.login, packet.password)
        
    def _on_user_disconnected(self, message):
        '''
        Выполняется при отключении пользователя.
        @param message: UserDisconnectedMessage
        '''
        logger.debug('removing authenticated user')
        connection_id = message.connection_id
        if connection_id in self._authenticated:
            del self._authenticated[connection_id]

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
