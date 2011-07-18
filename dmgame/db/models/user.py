# coding=utf8
'''
Модель пользователя.
@author: Mic, 2011
'''

from dmgame.db.models.base import Model

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
