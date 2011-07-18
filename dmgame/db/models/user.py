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
        self.login = None
        
    def __eq__(self, other):
        return self.login == other.login
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return '<User %s>'%self.login
