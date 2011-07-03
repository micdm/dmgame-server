# coding=utf8
'''
Рассылка сообщений.
@author: Mic, 2011
'''

from dmgame.messages import incoming, outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Dispatcher(object):
    '''
    Класс для рассылки сообщений.
    '''
    INCOMING_MESSAGES_TYPE = 'INCOMING'
    OUTCOMING_MESSAGES_TYPE = 'OUTCOMING'
    
    _subscription = {}

    @classmethod
    def _dispatch(cls, key, message):
        '''
        Вызывает коллбэки из подписки.
        @param key: mixed
        @param message: dmgame.messages.Message
        '''
        if key in cls._subscription:
            for callback in cls._subscription[key]:
                callback(message)

    @classmethod
    def dispatch(cls, message):
        '''
        Рассылает сообщение.
        @param text: dmgame.messages.Message
        '''
        logger.debug('dispatching message %s'%message)
        cls._dispatch(type(message), message)
        if isinstance(message, incoming.IncomingMessage):
            cls._dispatch(cls.INCOMING_MESSAGES_TYPE, message)
        if isinstance(message, outcoming.OutcomingMessage):
            cls._dispatch(cls.OUTCOMING_MESSAGES_TYPE, message)

    @classmethod
    def subscribe(cls, type, callback):
        '''
        Подписывает на сообщения определенного типа.
        @param type: mixed
        @param callback: function
        '''
        logger.debug('subscribing for messages of type "%s"'%type)
        if type not in cls._subscription:
            cls._subscription[type] = []
        cls._subscription[type].append(callback)

    @classmethod
    def unsubscribe(cls, type, callback):
        '''
        Отписывается от получения сообщений.
        @param type: mixed
        @param callback: function
        '''
        logger.debug('unsubscribing for messages of type "%s"'%type)
        if type in cls._subscription:
            if callback in cls._subscription[type]:
                cls._subscription[type].remove(callback)
