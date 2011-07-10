# coding=utf8
'''
Входящие Game-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.incoming import IncomingPacket

class GamePacket(IncomingPacket):
    '''
    Базовый абстрактный игровой пакет.
    '''

    namespace = 'game'
