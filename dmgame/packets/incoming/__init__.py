# coding=utf8
'''
Входящие пакеты (от клиента).
@author: Mic, 2011
'''

from dmgame.packets import Packet

class IncomingPacket(Packet):
    '''
    Базовый абстрактный класс для входящих пакетов.
    '''
    
    direction = 'incoming'

    def set_data(self, data):
        '''
        Заполняет пакет данными.
        @param data: dict
        '''


from dmgame.packets.incoming.auth import *
from dmgame.packets.incoming.hall import *

# Собираем все классы пакетов в словарь.
_types = {}
for var in locals().values():
    try:
        if issubclass(var, IncomingPacket):
            key = '%s:%s'%(var.namespace, var.type)
            _types[key] = var
    except:
        pass


def get_packet_class(namespace, type):
    '''
    Возвращает класс пакета.
    @param namespace: string
    @param type: string
    @return: type
    '''
    return _types.get('%s:%s'%(namespace, type))
