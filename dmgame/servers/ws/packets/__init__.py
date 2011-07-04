# coding=utf8
'''
Базовые вещи для пакетов данных.
@author: Mic, 2011
'''

class Packet(object):
    '''
    Базовый абстрактный класс пакета.
    '''
    
    def __str__(self):
        return '<%s>'%type(self).__name__
