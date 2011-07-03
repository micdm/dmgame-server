# coding=utf8
'''
Сериализация/десериализация сообщений.
@author: Mic, 2011
'''

from tornado.escape import json_decode, json_encode

import dmgame.messages.incoming as incoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Converter(object):
    '''
    Класс сериализации/десериализации сообщений.
    '''

    @classmethod
    def serialize(cls, message):
        '''
        Превращает сообщение в текст.
        @param message: dmgame.messages.Message
        @return: string
        '''
        try:
            return json_encode(message.get_dict())
        except:
            logger.debug('can not serialize message to text')
            return None
    
    @classmethod
    def _check_message_data(cls, data):
        '''
        Проверяет корректность данных сообщения.
        @param data: dict
        '''
        if 'type' not in data:
            raise Exception('message data must contain "type" field')
        
    @classmethod
    def _build_message(cls, data):
        '''
        Создает сообщение по набору данных.
        @param data: dict
        '''
        type = data['type']
        msg_class = incoming.get_message_class(type)
        if msg_class is None:
            logger.debug('message class with type "%s" not found'%type)
            return None
        message = msg_class()
        message.set_data(data.get('data'))
        return message

    @classmethod
    def unserialize(cls, text):
        '''
        Преобразовывает текст в сообщение.
        @param text: string
        @return: dmgame.messages.Message
        '''
        try:
            data = json_decode(text)
            cls._check_message_data(data)
            return cls._build_message(data)
        except Exception as e:
            logger.debug('can not unserialize text to message: %s'%e)
            return None
