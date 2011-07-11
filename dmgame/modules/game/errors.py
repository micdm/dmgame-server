# coding=utf8
'''
Ошибки в игровом модуле.
@author: Mic, 2011
'''

class GameError(Exception):
    '''
    Базовый класс для игровых ошибок.
    '''
    

class BadTurnDataError(GameError):
    '''
    Игрок прислал плохие данные для хода.
    '''
    
    
class UnallowedTurnError(GameError):
    '''
    Игрок пытается сделать недопустимый ход.
    '''
