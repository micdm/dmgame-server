# coding=utf8
'''
Модуль для игрового зала.
@author: Mic, 2011
'''

from dmgame.messages.dispatcher import Dispatcher
from dmgame.messages.messages import ServerResponseMessage, UserRequestMessage
from dmgame.servers.ws.packets import incoming, outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class HallManager(object):
    '''
    Игровой зал.
    '''

    def _dispatch_welcome_to_hall(self, connection_id):
        '''
        Отправляет приветствие вошедшему в игровой зал.
        @param connection_id: int
        '''
        logger.debug('handling hall request')
        packet = outcoming.HallPacket()
        message = ServerResponseMessage(connection_id, packet)
        Dispatcher.dispatch(message)

    def _on_user_request(self, message):
        '''
        Выполняется при запросе пользователя.
        @param message: Message
        '''
        packet = message.packet
        connection_id = message.connection_id
        if isinstance(packet, incoming.HallPacket):
            self._dispatch_welcome_to_hall(connection_id)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing hall manager')
        Dispatcher.subscribe(UserRequestMessage, self._on_user_request)
