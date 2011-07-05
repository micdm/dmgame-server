# coding=utf8
'''
Исходящие Auth-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.outcoming import OutcomingPacket

class AuthPacket(OutcomingPacket):
    '''
    Пакет на аутентификацию.
    '''

    namespace = 'auth'


class LoginStatusPacket(AuthPacket):
    '''
    Пакет со статусом аутентификации.
    '''

    STATUS_OK = 'OK'

    type = 'auth'

    def __init__(self, status, *args, **kwargs):
        self.status = status

    def _get_data(self):
        return {'status': self.status}
