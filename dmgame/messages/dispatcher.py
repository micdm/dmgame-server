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
    INCOMING_MESSAGES_TYPE = 'incoming'
    OUTCOMING_MESSAGES_TYPE = 'outcoming'
    
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
    def _subscribe(cls, key, callback):
        '''
        Добавляет коллбэк в подписку.
        @param key: mixed
        @param callback: function
        '''
        if key not in cls._subscription:
            cls._subscription[key] = []
        cls._subscription[key].append(callback)

    @classmethod
    def subscribe(cls, msg_class, callback):
        '''
        Подписывает на сообщения определенного типа.
        @param msg_class: dmgame.messages.Message
        @param callback: function
        '''
        logger.debug('subscribing for messages of type "%s"'%msg_class.type)
        cls._subscribe(msg_class, callback)
    
    @classmethod
    def subscribe_for_type(cls, type, callback):
        '''
        Подписывает на все сообщения указанного типа.
        @param type: string
        @param callback: function
        '''
        if type not in (cls.INCOMING_MESSAGES_TYPE, cls.OUTCOMING_MESSAGES_TYPE):
            raise Exception('unknown messages type "%s"'%type)
        cls._subscribe(type, callback)
