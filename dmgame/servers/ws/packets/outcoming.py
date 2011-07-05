# coding=utf8
'''
Исходящие пакеты (от сервера).
@author: Mic, 2011
'''

from dmgame.servers.ws.packets import Packet
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class OutcomingPacket(Packet):
    '''
    Базовый абстрактный класс для исходящих пакетов.
    '''
    def __str__(self):
        return '<outcoming:%s>'%self.type
    
    def _get_data(self):
        '''
        Возвращает данные пакета.
        @return: dict
        '''
        return None

    def get_dict(self):
        '''
        Строит словарь по данным пакета.
        @return: dict
        '''
        result = {'type': self.type}
        data = self._get_data()
        if data is not None:
            result['data'] = data
        return result


class AuthPacket(OutcomingPacket):
    '''
    Пакет со статусом аутентификации.
    '''
    STATUS_OK = 'OK'

    type = 'auth'
    def __init__(self, status, *args, **kwargs):
        super(AuthPacket, self).__init__(*args, **kwargs)
        self.status = status

    def _get_data(self):
        return {'status': self.status}
    
    
class HallPacket(OutcomingPacket):
    '''
    Пакет "добро пожаловать в игровой зал".
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
