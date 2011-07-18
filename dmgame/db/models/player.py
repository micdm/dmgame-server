# coding=utf8
'''
Модель игрока.
@author: Mic, 2011
'''

from dmgame.db.models.base import Model

class Player(Model):
    '''
    Игрок. Один зарегистрированный пользователь может играть из нескольких мест,
    поэтому игрок - это пользователь плюс конкретное соединение.
    '''
    
    def __init__(self, user, connection_id):
        '''
        @param user: User
        @param connection_id: int
        '''
        self.user = user
        self.connection_id = connection_id
        self.is_in_party = False
        self.is_in_game = False
        
    def __eq__(self, other):
        return self.connection_id == other.connection_id and self.user == other.user

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return '<Player #%s>'%self.connection_id
