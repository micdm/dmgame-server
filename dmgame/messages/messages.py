# coding=utf8
'''
Сообщения.
@author: Mic, 2011
'''

class MessageMeta(type):
    '''
    Для красивых принтов ;).
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

    def __init__(self, connection_id, packet):
        '''
        @param connection_id: int
        @param packet: dmgame.packets.incoming.IncomingPacket
        '''
        self.connection_id = connection_id
        self.packet = packet
        
        
class ClientDisconnectedMessage(Message):
    '''
    Клиент отключился.
    '''

    def __init__(self, connection_id):
        '''
        @param connection_id: int
        '''
        self.connection_id = connection_id
        
        
class ServerResponseMessage(Message):
    '''
    Отправляется сообщение от сервера.
    '''

    def __init__(self, connection_id, packet):
        '''
        @param connection_id: int
        @param packet: dmgame.packets.outcoming.OutcomingPacket
        '''
        self.connection_id = connection_id
        self.packet = packet
        
        
class UserRequestMessage(ClientRequestMessage):
    '''
    Получено сообщение от авторизованного пользователя.
    '''

    def __init__(self, user, connection_id, packet):
        '''
        @param user: User
        @param connection_id: int
        @param packet: IncomingPacket
        '''
        super(UserRequestMessage, self).__init__(connection_id, packet)
        self.user = user
        
        
class UserDisconnectedMessage(ClientDisconnectedMessage):
    '''
    Авторизованный пользователь отключился.
    '''

    def __init__(self, user, connection_id):
        '''
        @param user: User
        @param connection_id: int
        '''
        super(UserDisconnectedMessage, self).__init__(connection_id)
        self.user = user
