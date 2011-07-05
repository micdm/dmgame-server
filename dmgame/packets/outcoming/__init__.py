# coding=utf8
'''
Исходящие пакеты (от сервера).
@author: Mic, 2011
'''

from dmgame.packets import Packet

class OutcomingPacket(Packet):
    '''
    Базовый абстрактный класс для исходящих пакетов.
    '''

    direction = 'outcoming'

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
