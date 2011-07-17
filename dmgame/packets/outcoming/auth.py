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

    STATUS_OK = 'ok'
    STATUS_NOT_FOUND = 'not_found'

    type = 'login_status'

    def __init__(self, status, *args, **kwargs):
        self.status = status

    def _get_data(self):
        return {'status': self.status}
