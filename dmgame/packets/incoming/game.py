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


class PlayerTurnPacket(GamePacket):
    '''
    Игрок ходит.
    '''

    type = 'turn'
    
    def set_data(self, data):
        self.data = data
