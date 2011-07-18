# coding=utf8
'''
Модель члена игрового стола.
@author: Mic, 2011
'''

from dmgame.db.models.base import Model

class TableMember(Model):
    '''
    Член игрового стола.
    '''
    
    def __init__(self):
        '''
        @param number: int
        @param player: Player
        '''
        self.number = None
        self.player = None
        self.is_turning = False
        self.is_turning_first = False
        self.result = None
        
    def __str__(self):
        return str(self.player)
    
    def __eq__(self, other):
        return self.player == other.player
    
    def __ne__(self, other):
        return not self.__eq__(other)


class CardTableMember(TableMember):
    '''
    Член карточного игрового стола.
    '''
    
    def __init__(self, *args, **kwargs):
        super(CardTableMember, self).__init__(*args, **kwargs)
        self.hand = None