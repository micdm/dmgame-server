# coding=utf8
'''
Сообщения.
@author: Mic, 2011
'''

class MessageMeta(type):
    '''
    Для красивых принтов ;)
    '''

    def __str__(self):
        return '<%s>'%self.__name__


class Message(object):
    '''
    Базовый абстрактный класс сообщения.
    '''
    __metaclass__ = MessageMeta

    def __str__(self):
        return '<%s>'%type(self).__name__


class ClientRequestMessage(Message):
    '''
    Получено сообщение от клиента.
    '''

    def __init__(self, handler_id, packet):
        '''
        @param handler_id: int
        @param packet: dmgame.servers.ws.packets.incoming.IncomingPacket
        '''
        self.handler_id = handler_id
        self.packet = packet
        
        
class UserRequestMessage(ClientRequestMessage):
    '''
    Получено сообщение от авторизованного пользователя.
    '''

    def __init__(self, user, *args, **kwargs):
        '''
        @param user: object
        '''
        super(UserRequestMessage, self).__init__(*args, **kwargs)
        self.user = user


class ServerResponseMessage(Message):
    '''
    Отправляется сообщение от сервера.
    '''

    def __init__(self, handler_id, packet):
        '''
        @param handler_id: int
        @param packet: dmgame.servers.ws.packets.outcoming.OutcomingPacket
        '''
        self.handler_id = handler_id
        self.packet = packet


class ClientDisconnectedMessage(Message):
    '''
    Клиент отключился.
    '''

    def __init__(self, handler_id):
        '''
        @param handler_id: int
        '''
        self.handler_id = handler_id
