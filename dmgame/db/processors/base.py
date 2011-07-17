# coding=utf8
'''
Базовый процессор данных.
@author: Mic, 2011
'''

from functools import partial

from dmgame.db.client import DbClient
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class ModelProcessor(object):
    '''
    Базовый процессор моделей.
    '''
    
    # Класс модели:
    _model = None
    
    # Список полей, которые копируются напрямую:
    _fields = []

    @classmethod
    def model_to_dict(cls, model):
        '''
        Заполняет словарь по данным модели.
        @param model: Model
        @return: dict
        '''
        result = {}
        for field in cls._fields:
            result[field] = getattr(model, field)
        return result

    @classmethod
    def dict_to_model(cls, dict):
        '''
        Создает модель и заполняет ее по словарю.
        @param dict: dict
        @return: Model
        '''
        model = cls._model()
        for field in cls._fields:
            setattr(model, field, dict[field])
        return model


class DocumentProcessor(ModelProcessor):
    '''
    Базовый процессор документов.
    Умеет не только преобразовывать модели в словари и обратно, но и запрашивать и сохранять данные.
    '''

    # Название коллекции, в которой хранятся модели:
    _collection = None

    @classmethod
    def _call_on_find(cls, callback, response, error):
        '''
        Вызывается при появлении результатов.
        @param callback: function
        @param response: dict
        @param error: object
        '''
        if isinstance(response, list):
            if len(response):
                result = map(cls.dict_to_model, response)
            else:
                result = None
        else:
            result = cls.dict_to_model(response)
        if error is not None:
            logger.error(error)
        callback(result)

    @classmethod
    def find(cls, filter, callback):
        '''
        Ищет записи.
        @param filter: dict
        @param callback: callback
        @return: list
        '''
        on_results = partial(cls._call_on_find, callback)
        return DbClient.get_collection(cls._collection).find(filter, callback=on_results)
    
    @classmethod
    def find_one(cls, filter, callback):
        '''
        Ищет одну запись.
        @param filter: dict
        @param callback: callback
        @return: object
        '''
        on_results = partial(cls._call_on_find, callback)
        return DbClient.get_collection(cls._collection).find_one(filter, callback=on_results)
    
    @classmethod
    def _call_on_insert(cls, callback, response, error):
        '''
        Вызывается при добавлении записи.
        @param callback: function
        @param response: dict
        @param error: object
        '''
        if error is not None:
            logger.error(error)
        callback()

    @classmethod
    def save(cls, model, callback=None):
        '''
        Сохраняет модель в базу.
        @param model: Model
        '''
        data = cls.model_to_dict(model)
        if callback is None:
            callback = lambda: True
        on_result = partial(cls._call_on_insert, callback)
        DbClient.get_collection(cls._collection).save(data, callback=on_result)
