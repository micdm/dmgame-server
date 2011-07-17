# coding=utf8
'''
Основной сервер.
@author: Mic, 2011
'''
from functools import partial

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from dmgame import settings
from dmgame.messages.dispatcher import client_dispatcher
import dmgame.messages.messages as messages
import dmgame.packets.outcoming.misc as outcoming
from dmgame.servers.ws.converter import Converter
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Handler(WebSocketHandler):
    '''
    Обработчик соединений.
    '''
    def __init__(self, on_open, on_packet, on_close, *args, **kwargs):
        '''
        @param on_open: function
        @param on_packet: function
        @param on_close: function
        '''
        super(Handler, self).__init__(*args, **kwargs)
        self._on_open = on_open
        self._on_packet = on_packet
        self._on_close = on_close
    
    def open(self):
        '''
        Выполняется при подключении клиента.
        '''
        logger.debug('client connected from %s'%self.request.remote_ip)
        self._on_open()

    def on_message(self, text):
        '''
        Выполняется при получении сообщения.
        @param text: string
        '''
        logger.debug('received packet of length %s'%len(text))
        self._on_packet(text)
        
    def write_message(self, text):
        '''
        Отправляет сообщение клиенту.
        @param text: string
        '''
        logger.debug('sending packet of length %s'%len(text))
        return super(Handler, self).write_message(text)
            
    def on_close(self):
        '''
        Выполняется при отключении клиента.
        '''
        logger.debug('client disconnected from %s'%self.request.remote_ip)
        self._on_close()

        
class Server(object):
    '''
    Сервер.
    '''
    
    def __init__(self, address):
        super(Server, self).__init__()
        self._address = address
        self._next_handler_id = 0
        self._handlers = {}
        
    def _on_handler_open(self, handler_id):
        '''
        Проверяет количество текущих соединений.
        Если указанное соединение лишнее, закрывает его.
        @param handler_id: int
        '''
        count = len(self._handlers.values())
        max_count = settings.MAX_CONNECTION_COUNT
        if count > max_count:
            logger.debug('max connection count of %s exceeded, closing handler %s'%(max_count, handler_id))
            packet = outcoming.ServerBusyPacket()
            message = messages.ClientResponseMessage(handler_id, packet)
            client_dispatcher.dispatch(message)
            handler = self._handlers[handler_id]
            handler.close()
        
    def _on_handler_message(self, handler_id, text):
        '''
        Обрабатывает входящий пакет.
        @param handler_id: int
        @param text: string
        '''
        logger.debug('parsing packet of length %s'%len(text))
        packet = Converter.unserialize(text)
        if packet is not None:
            message = messages.ClientRequestMessage(handler_id, packet)
            client_dispatcher.dispatch(message)
        
    def _on_handler_close(self, handler_id):
        '''
        Удаляет обработчик соединения с указанным идентификатором.
        @param id: int
        '''
        logger.debug('removing handler #%s'%handler_id)
        message = messages.ClientDisconnectedMessage(handler_id)
        client_dispatcher.dispatch(message)
        del self._handlers[handler_id]

    def _create_handler(self, *args, **kwargs):
        '''
        Возвращает обработчик соединения.
        @return: Handler
        '''
        logger.debug('creating handler #%s'%self._next_handler_id)
        handler_id = self._next_handler_id
        # Создаем объект соединения:
        on_open = partial(self._on_handler_open, handler_id)
        on_packet = partial(self._on_handler_message, handler_id)
        on_close = partial(self._on_handler_close, handler_id)
        handler = Handler(on_open, on_packet, on_close, *args, **kwargs)
        # Сохраняем, инкрементируем счетчик:
        self._handlers[handler_id] = handler
        self._next_handler_id += 1
        return handler
        
    def _init_application(self):
        '''
        Возвращает приложение.
        @return: Application
        '''
        application = Application([
            (r'/', self._create_handler),
        ], debug=settings.DEBUG)
        application.listen(self._address[1], self._address[0])
        
    def _on_client_response(self, message):
        '''
        Выполняется при появлении исходящего сообщения.
        @param message: ClientResponseMessage
        '''
        handler_id = message.connection_id
        packet = message.packet
        logger.debug('sending packet %s to handler #%s'%(packet, handler_id))
        text = Converter.serialize(packet)
        if text is not None and handler_id in self._handlers:
            try:
                self._handlers[handler_id].write_message(text)
            except IOError as e:
                logger.debug('error on writing message: %s'%e)

    def _init_subscription(self):
        '''
        Инициализирует подписку.
        '''
        client_dispatcher.subscribe(messages.ClientResponseMessage, self._on_client_response)
        
    def _init_loop(self):
        '''
        Запускает цикл.
        '''
        try:
            IOLoop.instance().start()
        except KeyboardInterrupt:
            logger.info('stopping websockets server')

    def init(self):
        '''
        Запускает сервер.
        '''
        logger.info('starting websockets server on %s:%s'%self._address)
        self._init_application()
        self._init_subscription()
        self._init_loop()
