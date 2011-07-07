# coding=utf8
'''
Базовые вещи для пакетов данных.
@author: Mic, 2011
'''

class PacketMeta(type):
    '''
    Для красивых принтов ;).
    '''

    def __str__(self):
        return '<%s:%s:%s>'%(self.direction, self.namespace, self.type)


class Packet(object):
    '''
    Базовый абстрактный класс пакета.
    '''
    
    __metaclass__ = PacketMeta

    def __str__(self):
        return '<%s:%s:%s>'%(self.direction, self.namespace, self.type)
