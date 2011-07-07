# coding=utf8
'''
Рассылка сообщений.
@author: Mic, 2011
'''

import dmgame.messages.messages as messages
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Dispatcher(object):
    '''
    Абстрактный класс для рассылки сообщений.
    '''

    def __init__(self):
        self._subscription = {}
        self._packets_subscription = {}        
    
    def _dispatch(self, subscription, key, message):
        '''
        Вызывает коллбэки.
        @param subscription: dict
        @param key: mixed
        @param message: Message
        '''
        if key in subscription:
            for callback in subscription[key]:
                callback(message)

    def _subscribe(self, subscription, key, callback):
        '''
        Добавляет новую подписку.
        @param subscription: dict
        @param key: object
        @param callback: function
        '''
        if key not in subscription:
            subscription[key] = []
        subscription[key].append(callback)

    def _unsubscribe(self, subscription, key, callback):
        '''
        Удаляет подписку.
        @param subscription: dict
        @param key: object
        @param callback: function
        '''
        if key in subscription:
            if callback in subscription[key]:
                subscription[key].remove(callback)
                
    def _get_trigger_message(self):
        '''
        Возвращает тип сообщений, на которые будет срабатывать проверка пакета.
        @return: Message
        '''
        raise NotImplementedError()

    def dispatch(self, message):
        '''
        Рассылает сообщение.
        @param message: Message
        '''
        logger.debug('dispatching message %s'%message)
        self._dispatch(self._subscription, type(message), message)
        if isinstance(message, self._get_trigger_message()):
            packet = message.packet
            logger.debug('dispatching packet message %s'%packet)
            self._dispatch(self._packets_subscription, type(packet), message)

    def subscribe(self, message_type, callback):
        '''
        Подписывает на сообщения определенного типа.
        @param message_type: Message
        @param callback: function
        '''
        logger.debug('subscribing for messages of type %s'%message_type)
        self._subscribe(self._subscription, message_type, callback)

    def unsubscribe(self, message_type, callback):
        '''
        Отписывается от получения сообщений.
        @param message_type: mixed
        @param callback: function
        '''
        logger.debug('unsubscribing from messages of type %s'%message_type)
        self._unsubscribe(self._subscription, message_type, callback)

    def subscribe_for_packet(self, packet_type, callback):
        '''
        Подписывается на определенные входящие пакеты.
        @param packet_type: IncomingPacket
        @param callback: function
        '''
        logger.debug('subscribing for packets of type %s'%packet_type)
        self._subscribe(self._packets_subscription, packet_type, callback)

    def unsubscribe_from_packet(self, packet_type, callback):
        '''
        Отписывается от определенных входящих пакетов.
        @param packet_type: IncomingPacket
        @param callback: function
        '''
        logger.debug('unsubscribing from packets of type %s'%packet_type)
        self._unsubscribe(self._packets_subscription, packet_type, callback)


class ClientDispatcher(Dispatcher):
    '''
    Клиентский диспетчер.
    '''
    
    def _get_trigger_message(self):
        return messages.ClientRequestMessage

    
class UserDispatcher(Dispatcher):
    '''
    Пользовательский диспетчер.
    '''
    
    def _get_trigger_message(self):
        return messages.UserRequestMessage
    

class PlayerDispatcher(Dispatcher):
    '''
    Игровой диспетчер.
    '''
    
    def _get_trigger_message(self):
        return messages.PlayerRequestMessage


# Как бы синглтоны:
user_dispatcher = UserDispatcher()
client_dispatcher = ClientDispatcher()
player_dispatcher = PlayerDispatcher()
