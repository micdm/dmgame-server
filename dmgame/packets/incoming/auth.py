# coding=utf8
'''
Входящие Auth-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.incoming import IncomingPacket

class AuthPacket(IncomingPacket):
    '''
    Базовый абстрактный пакет на аутентификацию.
    '''

    namespace = 'auth'


class LoginPacket(AuthPacket):
    '''
    Пакет на аутентификацию.
    '''

    type = 'login'

    def set_data(self, data):
        self.login = data['login']
        self.password = data['password']
