# coding=utf8
'''
Входящие Hall-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.incoming import IncomingPacket

class HallPacket(IncomingPacket):
    '''
    Пакет для работы с игровым залом.
    '''

    namespace = 'hall'


class EnterPacket(HallPacket):
    '''
    Вход в зал.
    '''

    type = 'enter'
