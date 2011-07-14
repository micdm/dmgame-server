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
from dmgame.servers.ws.converter import Converter
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Handler(WebSocketHandler):
    '''
    Обработчик соединений.
    '''
    def __init__(self, on_packet, on_close, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self._on_packet = on_packet
        self._on_close = on_close
    
    def open(self):
        '''
        Выполняется при подключении клиента.
        '''
        logger.debug('client connected from %s'%self.request.remote_ip)

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
        
    def _parse_packet(self, handler_id, text):
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
        
    def _close_handler(self, handler_id):
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
        on_packet = partial(self._parse_packet, self._next_handler_id)
        on_close = partial(self._close_handler, self._next_handler_id)
        handler = Handler(on_packet, on_close, *args, **kwargs)
        # TODO: ограничить количество одновременных соединений.
        self._handlers[self._next_handler_id] = handler
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
            self._handlers[handler_id].write_message(text)
        
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
