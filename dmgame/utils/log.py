# coding=utf8
'''
Логирование.
@author: Mic, 2011
'''

import logging

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


def get_logger(name):
    '''
    Настраивает и возвращает логгер.
    @param name: string
    @return: logging.Logger
    '''
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_get_handler())
    return logger
