# coding=utf8
'''
Клиент БД.
@author: Mic, 2011
'''

from pymongo import Connection

from dmgame import settings

class DbClient(object):
    '''
    Клиент БД.
    '''

    # Объект для работы с БД:
    _db = None

    @classmethod
    def get_db(cls):
        '''
        Возвращает объект для работы с БД.
        @return: object
        '''
        if cls._db is None:
            connection = Connection(settings.MONGODB_HOST, settings.MONGODB_PORT)
            cls._db = connection[settings.MONGODB_DB_NAME]
        return cls._db

    @classmethod
    def get_collection(cls, name):
        '''
        Возвращает объект коллекции.
        @param name: string
        @return: object
        '''
        return getattr(cls.get_db(), name)
