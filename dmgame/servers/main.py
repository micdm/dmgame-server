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
from dmgame.auth import AuthManager
from dmgame.messages.converter import Converter
from dmgame.messages.dispatcher import Dispatcher
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Handler(WebSocketHandler):
    '''
    Обработчик соединений.
    '''
    def __init__(self, on_message, on_close, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self._on_message = on_message
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
        logger.debug('received message of length %s'%len(text))
        self._on_message(text)
        
    def write_message(self, text):
        '''
        Отправляет сообщение клиенту.
        @param text: string
        '''
        logger.debug('sending message of length %s'%len(text))
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
        
    def _parse_message(self, handler_id, text):
        '''
        Обрабатывает входящее сообщение.
        @param handler_id: int
        @param text: string
        '''
        logger.debug('parsing message of length %s'%len(text))
        message = Converter.unserialize(text)
        if message is not None:
            message.handler_id = handler_id
            Dispatcher.dispatch(message)
        else:
            logger.debug('message not dispatched')
        
    def _close_handler(self, handler_id):
        '''
        Удаляет обработчик соединения с указанным идентификатором.
        @param id: int
        '''
        logger.debug('removing handler #%s'%handler_id)
        del self._handlers[handler_id]
    
    def _create_handler(self, *args, **kwargs):
        '''
        Возвращает обработчик соединения.
        @return: Handler
        '''
        logger.debug('creating handler #%s'%self._next_handler_id)
        on_message = partial(self._parse_message, self._next_handler_id)
        on_close = partial(self._close_handler, self._next_handler_id)
        handler = Handler(on_message, on_close, *args, **kwargs)
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
        
    def _on_outcoming_message(self, message):
        '''
        Выполняется при появлении исходящего сообщения.
        @param message: dmgame.message.outcoming.OutcomingMessage
        '''
        text = Converter.serialize(message)
        if text is not None:
            handler_id = message.handler_id
            if handler_id in self._handlers:
                self._handlers[handler_id].write_message(text)
        else:
            logger.debug('message not sent')
        
    def _init_subscription(self):
        '''
        Инициализирует подписку.
        '''
        Dispatcher.subscribe(Dispatcher.OUTCOMING_MESSAGES_TYPE, self._on_outcoming_message)
        
    def _init_modules(self):
        '''
        Инициализирует модули.
        '''
        AuthManager().init()

    def start(self):
        '''
        Запускает сервер.
        '''
        logger.info('starting main server on %s:%s'%self._address)
        self._init_application()
        self._init_subscription()
        self._init_modules()
        
    def stop(self):
        '''
        Останавливает сервер.
        '''
        logger.info('stopping main server')


def start_server():
    '''
    Запускает сервер.
    '''
    server = Server(settings.SERVERS['main'])
    server.start()
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        server.stop()
