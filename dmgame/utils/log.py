# coding=utf8
'''
Логирование.
@author: Mic, 2011
'''

import logging

from dmgame.settings import ENABLE_LOGGING_FOR

def _get_formatter():
    '''
    Возвращает форматировщик.
    @return: logging.Formatter
    '''
    return logging.Formatter('%(asctime)s [%(levelname)s] [%(module)s] %(message)s')


def _get_handler():
    '''
    Возвращает обработчик.
    @return: logging.Handler
    '''
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(_get_formatter())
    return handler


def _need_enable_logger(name):
    '''
    Нужно ли включить логгер?
    @param name: string
    @return: bool
    '''
    if ENABLE_LOGGING_FOR is None:
        return True
    for module in ENABLE_LOGGING_FOR:
        if name.startswith(module):
            return True
    return False


def get_logger(name):
    '''
    Настраивает и возвращает логгер.
    @param name: string
    @return: logging.Logger
    '''
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    if _need_enable_logger(name):
        logger.addHandler(_get_handler())
    else:
        logger.disabled = True
    return logger
