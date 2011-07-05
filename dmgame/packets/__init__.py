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
        return '<%s:%s:%s>'%(self.direction, self.namespace, self.type)

