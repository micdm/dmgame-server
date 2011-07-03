# coding=utf8
'''
Рассылка сообщений.
@author: Mic, 2011
'''

from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Dispatcher(object):
    '''
    Класс для рассылки сообщений.
    '''
    _subscription = {}

    @classmethod
    def dispatch(cls, message):
        '''
        Рассылает сообщение.
        @param text: dmgame.messages.messages.Message
        '''
        logger.debug('dispatching message %s'%message)
        key = type(message)
        if key in cls._subscription:
            for callback in cls._subscription[key]:
                callback(message)

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
