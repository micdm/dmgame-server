# coding=utf8
'''
Таймер
@author: Mic, 2011
'''

from time import time

from tornado.ioloop import IOLoop

class Timer(object):
    '''
    Таймер.
    '''
    
    def __init__(self, interval, callback):
        '''
        @param interval: float
        @param callback: function
        '''
        self._deadline = time() + interval
        self._callback = callback
        self._timeout = None
    
    def start(self):
        '''
        Запускает таймер.
        '''
        self._timeout = IOLoop.instance().add_timeout(self._deadline, self._callback)
    
    def stop(self):
        '''
        Останавливает таймер.
        '''
        IOLoop.instance().remove_timeout(self._timeout)
