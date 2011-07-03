# coding=utf8
'''
Входящие сообщения (от клиента).
@author: Mic, 2011
'''

from dmgame.messages import Message
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class HelloMessage(Message):
    '''
    Тестовое сообщение.
    '''
    
    type = 'hello'
    
    def set_data(self, data):
        logger.debug('message data is "%s"'%data)
    

# Заполняем словарь для быстрого поиска в дальнейшем:
_types = {}
for msg_class in (HelloMessage,):
    _types[msg_class.type] = msg_class


def get_message_class(type):
    '''
    Возвращает класс сообщения по указанному типу.
    @param type: string
    @return: type
    '''
    return _types.get(type)
