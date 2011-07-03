# coding=utf8
'''
Базовые вещи для системы сообщений.
@author: Mic, 2011
'''

class Message(object):
    '''
    Базовый абстрактный класс сообщения.
    '''

    def set_data(self, data):
        '''
        Заполняет поля сообщения.
        @param data: dict
        '''
        raise NotImplementedError()
