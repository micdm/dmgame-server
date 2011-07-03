# coding=utf8
'''
Исходящие сообщения (от сервера).
@author: Mic, 2011
'''

from dmgame.messages import Message
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class OutcomingMessage(Message):
    '''
    Базовый абстрактный класс для исходящих сообщений.
    '''
    def __str__(self):
        return '"outcoming:%s"'%self.type
    
    def _get_data(self):
        '''
        Возвращает данные сообщения.
        @return: dict
        '''
        return None

    def get_dict(self):
        '''
        Строит словарь по данным сообщения.
        @return: dict
        '''
        result = {'type': self.type}
        data = self._get_data()
        if data is not None:
            result['data'] = data
        return result


class AuthMessage(OutcomingMessage):
    '''
    Сообщение со статусом аутентификации.
    '''
    type = 'auth'
    def __init__(self, key, *args, **kwargs):
        super(AuthMessage, self).__init__(*args, **kwargs)
        self._key = key

    def _get_data(self):
        return {'key': self._key}

# Заполняем словарь для быстрого поиска в дальнейшем:
_types = {}
for msg_class in (AuthMessage,):
    _types[msg_class.type] = msg_class


def get_message_class(type):
    '''
    Возвращает класс сообщения по указанному типу.
    @param type: string
    @return: type
    '''
    return _types.get(type)
