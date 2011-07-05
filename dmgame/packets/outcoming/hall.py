# coding=utf8
'''
Исходящие Hall-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.outcoming import OutcomingPacket

class HallPacket(OutcomingPacket):
    '''
    Игровой зал.
    '''

    namespace = 'hall'


class WelcomePacket(HallPacket):
    '''
    Добро пожаловать в игровой зал.
    '''

    type = 'hall'

    def _get_data(self):
        '''
        Тут будет информация о зале - количество участников, доступные столы,
        прочая игровая информация. 
        '''
