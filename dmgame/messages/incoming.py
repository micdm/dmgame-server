# coding=utf8
'''
Входящие сообщения (от клиента).
@author: Mic, 2011
'''

from dmgame.messages import Message
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class IncomingMessage(Message):
    '''
    Базовый абстрактный класс для входящих сообщений.
    '''
    def __str__(self):
        return '"incoming:%s"'%self.type
    
    def set_data(self, data):
        '''
        Заполняет сообщение данными.
        @param data: dict
        '''
        pass


class HelloMessage(IncomingMessage):
    '''
    Тестовое сообщение.
    '''
    type = 'hello'
    def set_data(self, data):
        logger.debug('message data is "%s"'%data)
        
        
class AuthMessage(IncomingMessage):
    '''
    Сообщение на аутентификацию.
    '''
    type = 'auth'
    def set_data(self, data):
        self.login = data['login']
        self.password = data['password']
    

# Заполняем словарь для быстрого поиска в дальнейшем:
_types = {}
for msg_class in (HelloMessage, AuthMessage):
    _types[msg_class.type] = msg_class


def get_message_class(type):
    '''
    Возвращает класс сообщения по указанному типу.
    @param type: string
    @return: type
    '''
    return _types.get(type)
