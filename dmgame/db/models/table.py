# coding=utf8
'''
Модель игрового стола.
@author: Mic, 2011
'''

from dmgame.db.models.base import Model

class GamblingTable(Model):
    '''
    Модель игрового стола.
    '''

    def __init__(self):
        self.members = {}
        self.is_ended = False
        
    def get_players(self):
        '''
        Возвращает список игроков.
        @return: list
        '''
        return self.members.keys()
    
    def has_player(self, player):
        '''
        Возвращает, есть ли игрок за столом.
        @param player: Player
        @return: bool
        '''
        return player in self.get_players()

    def get_members(self):
        '''
        Возвращает список игроков.
        @return: list
        '''
        return self.members.values()
    
    def get_member_by_player(self, player):
        '''
        Возвращает члена стола для игрока.
        @param player: Player
        @return: TableMember
        '''
        return self.members[player]
    
    def set_members(self, members):
        '''
        Сохраняет список игроков.
        @param members: list
        '''
        for member in members:
            self.members[member.player] = member
