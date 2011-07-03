# coding=utf8
'''
Сервер для раздачи Flash-политики через сокет.
@author: Mic, 2011
'''

import socket

from dmgame import settings
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

POLICY_HOST = settings.SERVERS['main'][0]
POLICY_PORT = 843

def _get_policy():
    '''
    Возвращает текст политики.
    @return: string
    '''
    return '''
        <?xml version="1.0"?>
        <cross-domain-policy>
            <allow-access-from domain="%s" to-ports="%s"/>
        </cross-domain-policy>
    '''%settings.SERVERS['main']


def start_server():
    '''
    Запускает сервер.
    '''
    server_address = (POLICY_HOST, POLICY_PORT)
    logger.info('starting policy server on %s:%s'%server_address)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(server_address)
    s.listen(1)
    try:
        while True:
            connection, address = s.accept()
            logger.debug('client connected from %s:%s'%address)
            connection.send(_get_policy())
            connection.close()
    except KeyboardInterrupt:
        pass
    logger.info('stopping policy server')
