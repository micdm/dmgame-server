# coding=utf8
'''
Модели данных.
@author: Mic, 2011
'''

class Model(object):
    '''
    Базовая абстрактная модель.
    '''


class User(Model):
    '''
    Модель пользователя.
    '''
    
    def __init__(self):
        self.id = None
        self.login = None
        
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return '<User %s (#%s)>'%(self.login, self.id)


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


class TableMember(object):
    '''
    Член игрового стола.
    '''
    
    def __init__(self, number, player):
        '''
        @param number: int
        @param player: Player
        '''
        self.number = number
        self.player = player
        self.is_turning = False
        self.is_turning_first = False
        self.result = None
        
    def __str__(self):
        return str(self.player)
    
    def __eq__(self, other):
        return self.player == other.player
    
    def __ne__(self, other):
        return not self.__eq__(other)
