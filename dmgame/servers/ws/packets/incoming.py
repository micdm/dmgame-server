# coding=utf8
'''
Входящие пакеты (от клиента).
@author: Mic, 2011
'''

from dmgame.servers.ws.packets import Packet
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class IncomingPacket(Packet):
    '''
    Базовый абстрактный класс для входящих пакетов.
    '''
    def __str__(self):
        return '<incoming:%s>'%self.type
    
    def set_data(self, data):
        '''
        Заполняет пакет данными.
        @param data: dict
        '''


class AuthPacket(IncomingPacket):
    '''
    Пакет на аутентификацию.
    '''
    type = 'auth'
    def set_data(self, data):
        self.login = data['login']
        self.password = data['password']
        
        
class HallPacket(IncomingPacket):
    '''
    Пакет на вход в игровой зал.
    '''
    type = 'hall'
    

# Заполняем словарь для быстрого поиска в дальнейшем:
_types = {}
for packet_class in (AuthPacket, HallPacket):
    _types[packet_class.type] = packet_class


def get_packet_class(type):
    '''
    Возвращает класс пакета по указанному типу.
    @param type: string
    @return: type
    '''
    return _types.get(type)
