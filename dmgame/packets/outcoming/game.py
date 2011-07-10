# coding=utf8
'''
Исходящие Game-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.outcoming import OutcomingPacket

class GamePacket(OutcomingPacket):
    '''
    Базовый абстрактный класс.
    '''

    namespace = 'game'
