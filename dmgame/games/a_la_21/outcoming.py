# coding=utf8
'''
Исходящие пакеты для игры.
@author: Mic, 2011
'''

from dmgame.packets.outcoming.game import GamePacket

class Packet(GamePacket):
    '''
    Базовый абстрактный класс для пакетов игры.
    '''
    
    namespace = 'a_la_21'


class SetHandValuePacket(Packet):
    '''
    Сумма карт игрока.
    '''
    
    type = 'set_hand_value'
    
    def __init__(self, member, value):
        '''
        @param member: TableMember
        @param value: int
        '''
        self.member = member
        self.value = value
    
    def _get_data(self):
        return {'id': self.member.number, 'value': self.value}
