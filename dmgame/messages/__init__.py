# coding=utf8
'''
Базовые вещи для системы сообщений.
@author: Mic, 2011
'''

class Message(object):
    '''
    Базовый абстрактный класс сообщения.
    '''
    def __init__(self):
        super(Message, self).__init__()
        self.handler_id = None
