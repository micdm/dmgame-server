# coding=utf8
'''
Рассылка сообщений.
@author: Mic, 2011
'''

import dmgame.messages.messages as messages
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Listener(object):
    
    def __init__(self, callback, group=None):
        '''
        @param callback: function
        @param group: object
        '''
        self.callback = callback
        self.group = group


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
            for listener in subscription[key]:
                listener.callback(message)

    def _subscribe(self, subscription, key, callback, group=None):
        '''
        Добавляет новую подписку.
        @param subscription: dict
        @param key: object
        @param callback: function
        @param group: object
        '''
        if key not in subscription:
            subscription[key] = []
        listener = Listener(callback, group)
        subscription[key].append(listener)

    def _unsubscribe(self, subscription, key=None, callback=None, group=None):
        '''
        Удаляет подписку.
        @param subscription: dict
        @param key: object
        @param callback: function
        @param group: object
        '''
        if group is not None:
            for listeners in subscription.values():
                for listener in list(listeners):
                    if listener.group == group:
                        listeners.remove(listener)
        elif key is not None and key in subscription:
            for listener in list(subscription[key]):
                if listener.callback == callback:
                    subscription[key].remove(listener)
        else:
            raise Exception('not enough parameters for unsubscription')
                
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

    def subscribe(self, message_type, callback, group=None):
        '''
        Подписывает на сообщения определенного типа.
        @param message_type: Message
        @param callback: function
        @param group: object
        '''
        logger.debug('subscribing for messages of type %s'%message_type)
        self._subscribe(self._subscription, message_type, callback, group)

    def unsubscribe(self, message_type, callback):
        '''
        Отписывается от получения сообщений.
        @param message_type: object
        @param callback: function
        '''
        logger.debug('unsubscribing from messages of type %s'%message_type)
        self._unsubscribe(self._subscription, message_type, callback)

    def subscribe_for_packet(self, packet_type, callback, group=None):
        '''
        Подписывается на определенные входящие пакеты.
        @param packet_type: IncomingPacket
        @param callback: function
        @param group: object
        '''
        logger.debug('subscribing for packets of type %s'%packet_type)
        self._subscribe(self._packets_subscription, packet_type, callback, group)

    def unsubscribe_from_packet(self, packet_type, callback):
        '''
        Отписывается от определенных входящих пакетов.
        @param packet_type: IncomingPacket
        @param callback: function
        '''
        logger.debug('unsubscribing from packets of type %s'%packet_type)
        self._unsubscribe(self._packets_subscription, packet_type, callback)
        
    def unsubscribe_from_all(self, group):
        '''
        Отписывается от всех сообщений.
        @param group: object
        '''
        logger.debug('unsubscribing from all messages')
        self._unsubscribe(self._subscription, group=group)
        self._unsubscribe(self._packets_subscription, group=group)


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
