# coding=utf8
'''
Сообщения.
@author: Mic, 2011
'''

class Message(object):
    '''
    Базовый абстрактный класс сообщения.
    '''


class ClientRequestMessage(Message):
    '''
    Получено сообщение от клиента.
    '''
    def __init__(self, handler_id, packet):
        self.handler_id = handler_id
        self.packet = packet


class ServerResponseMessage(Message):
    '''
    Отправляется сообщение от сервера.
    '''
    def __init__(self, handler_id, packet):
        self.handler_id = handler_id
        self.packet = packet


class ClientDisconnectedMessage(Message):
    '''
    Клиент отключился.
    '''
    def __init__(self, handler_id):
        self.handler_id = handler_id
