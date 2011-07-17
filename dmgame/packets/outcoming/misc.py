# coding=utf8
'''
Различные исходящие пакеты.
@author: Mic, 2011
'''

from dmgame.packets.outcoming import OutcomingPacket

class ServerBusyPacket(OutcomingPacket):
    '''
    Сервер не может принять новое соединение.
    '''

    namespace = 'server'
    type = 'busy'
