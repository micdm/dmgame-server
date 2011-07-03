# coding=utf8
'''
Основной сервер.
@author: Mic, 2011
'''

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from dmgame import settings
from dmgame.messages.converter import Converter
from dmgame.messages.dispatcher import Dispatcher
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Handler(WebSocketHandler):
    '''
    Обработчик соединений.
    '''
    
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
        message = Converter.unserialize(text)
        if message is not None:
            Dispatcher.dispatch(message)
        else:
            logger.debug('message not dispatched')
            
    def on_close(self):
        '''
        Выполняется при отключении клиента.
        '''
        logger.debug('client disconnected from %s'%self.request.remote_ip)
        
        
def _get_application():
    '''
    Возвращает приложение.
    @return: Application
    '''
    return Application([
        (r'/', Handler),
    ], debug=settings.DEBUG)


def start_server():
    '''
    Запускает сервер.
    '''
    server_address = settings.SERVERS['main']
    logger.info('starting main server on %s:%s'%server_address)
    application = _get_application()
    application.listen(server_address[1], server_address[0])
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    logger.info('stopping main server')
