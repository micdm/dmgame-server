# coding=utf8
'''
Рассылка сообщений.
@author: Mic, 2011
'''

from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Dispatcher(object):
    '''
    Класс для рассылки сообщений.
    '''

    @classmethod
    def dispatch(cls, message):
        '''
        Рассылает сообщение.
        @param text: dmgame.messages.Message
        '''
        logger.debug('message %s ready for dispatching'%message)
