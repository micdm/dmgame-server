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
        @param text: dmgame.messages.Message
        '''
        logger.debug('dispatching message of type "%s"'%message.type)
        msg_class = type(message)
        if msg_class in cls._subscription:
            for callback in cls._subscription[msg_class]:
                callback(message)

    @classmethod
    def subscribe(cls, msg_class, callback):
        '''
        Подписывает на сообщения определенного типа.
        @param msg_class: dmgame.messages.Message
        @param callback: function
        '''
        logger.debug('subscribing for messages of type %s'%msg_class.type)
        if msg_class not in cls._subscription:
            cls._subscription[msg_class] = []
        cls._subscription[msg_class].append(callback)
