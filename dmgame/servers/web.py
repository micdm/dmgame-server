# coding=utf8
'''
Сервер для раздачи страниц.
@author: Mic, 2011
'''

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from dmgame import settings
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Handler(RequestHandler):
    '''
    Обработчик соединений.
    '''

    def get(self):
        return self.render('%s/index.html'%settings.TEMPLATE_DIR)
        
        
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
    server_address = settings.SERVERS['web']
    logger.info('starting web server on %s:%s'%server_address)
    application = _get_application()
    application.listen(server_address[1], server_address[0])
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    logger.info('stopping web server')
