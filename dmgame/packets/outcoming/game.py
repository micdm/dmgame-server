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


class GameStartedPacket(GamePacket):
    '''
    Игра началась.
    '''
    
    type = 'game_started'

    def __init__(self, member, all_members):
        '''
        @param member: TableMember
        @param all_members: list
        '''
        self.member = member
        self.all_members = all_members

    def _get_data(self):
        return {
            'id': self.member.player.connection_id,
            'members': [member.player.connection_id for member in self.all_members]
        }


class MemberTurningPacket(GamePacket):
    '''
    Ход переходит к указанному игроку.
    '''
    
    type = 'member_turning'

    def __init__(self, member):
        '''
        @param member: TableMember
        '''
        self.member = member

    def _get_data(self):
        return {'member': self.member.player.connection_id}
