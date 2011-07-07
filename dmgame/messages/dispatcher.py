# coding=utf8
'''
Рассылка сообщений.
@author: Mic, 2011
'''

from dmgame.messages.messages import UserRequestMessage
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Dispatcher(object):
    '''
    Класс для рассылки сообщений.
    '''
    _subscription = {}
    _user_requests_subscription = {}
    
    @classmethod
    def _dispatch(cls, subscription, key, message):
        '''
        Вызывает коллбэки.
        @param subscription: dict
        @param key: mixed
        @param message: Message
        '''
        if key in subscription:
            for callback in subscription[key]:
                callback(message)
    
    @classmethod
    def _subscribe(cls, subscription, key, callback):
        '''
        Добавляет новую подписку.
        @param subscription: dict
        @param key: object
        @param callback: function
        '''
        if key not in subscription:
            subscription[key] = []
        subscription[key].append(callback)
    
    @classmethod
    def _unsubscribe(cls, subscription, key, callback):
        '''
        Удаляет подписку.
        @param subscription: dict
        @param key: object
        @param callback: function
        '''
        if key in subscription:
            if callback in subscription[key]:
                subscription[key].remove(callback)

    @classmethod
    def dispatch(cls, message):
        '''
        Рассылает сообщение.
        @param text: dmgame.messages.messages.Message
        '''
        logger.debug('dispatching message %s'%message)
        cls._dispatch(cls._subscription, type(message), message)
        if isinstance(message, UserRequestMessage):
            packet = message.packet
            logger.debug('dispatching user request %s'%packet)
            cls._dispatch(cls._user_requests_subscription, type(packet), message)

    @classmethod
    def subscribe(cls, message_type, callback):
        '''
        Подписывает на сообщения определенного типа.
        @param message_type: Message
        @param callback: function
        '''
        logger.debug('subscribing for messages of type %s'%message_type)
        cls._subscribe(cls._subscription, message_type, callback)

    @classmethod
    def unsubscribe(cls, message_type, callback):
        '''
        Отписывается от получения сообщений.
        @param message_type: mixed
        @param callback: function
        '''
        logger.debug('unsubscribing from messages of type %s'%message_type)
        cls._unsubscribe(cls._subscription, message_type, callback)

    @classmethod
    def subscribe_for_user_request(cls, packet_type, callback):
        '''
        Подписывается на определенные запросы пользователя.
        @param packet_type: IncomingPacket
        @param callback: function
        '''
        logger.debug('subscribing for user requests of type %s'%packet_type)
        cls._subscribe(cls._user_requests_subscription, packet_type, callback)
        
    @classmethod
    def unsubscribe_from_user_request(cls, packet_type, callback):
        '''
        Отписывается от определенных запросов пользователя.
        @param packet_type: IncomingPacket
        @param callback: function
        '''
        logger.debug('unsubscribing from user requests of type %s'%packet_type)
        cls._unsubscribe(cls._user_requests_subscription, packet_type, callback)
