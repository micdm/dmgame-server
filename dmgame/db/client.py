# coding=utf8
'''
Клиент БД.
@author: Mic, 2011
'''

from asyncmongo import Client

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
            cls._db = Client(pool_id=settings.MONGODB_POOL_ID, host=settings.MONGODB_HOST,
                             port=settings.MONGODB_PORT, dbname=settings.MONGODB_DB_NAME)
        return cls._db

    @classmethod
    def get_collection(cls, name):
        '''
        Возвращает объект коллекции.
        @param name: string
        @return: object
        '''
        return getattr(cls.get_db(), name)
