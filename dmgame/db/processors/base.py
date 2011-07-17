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

    @classmethod
    def _model_to_dict(cls, model):
        '''
        Заполняет словарь по данным модели.
        @param model: Model
        @return: dict
        '''
        raise NotImplementedError()

    @classmethod
    def _dict_to_model(cls, dict):
        '''
        Создает модель и заполняет ее по словарю.
        @param dict: dict
        @return: Model
        '''
        raise NotImplementedError()


class DocumentProcessor(ModelProcessor):
    '''
    Базовый процессор документов.
    Умеет не только преобразовывать модели в словари и обратно, но и запрашивать и сохранять данные.
    '''

    # Название коллекции, в которой хранятся модели:
    COLLECTION = None

    @classmethod
    def _call_on_results(cls, callback, response, error):
        '''
        Вызывается при появлении результатов.
        @param callback: function
        @param response: dict
        @param error: object
        '''
        if isinstance(response, list):
            if len(response):
                result = map(cls._dict_to_model, response)
            else:
                result = None
        else:
            result = cls._dict_to_model(response)
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
        on_results = partial(cls._call_on_results, callback)
        return DbClient.get_collection(cls.COLLECTION).find(filter, callback=on_results)
    
    @classmethod
    def find_one(cls, filter, callback):
        '''
        Ищет одну запись.
        @param filter: dict
        @param callback: callback
        @return: object
        '''
        on_results = partial(cls._call_on_results, callback)
        return DbClient.get_collection(cls.COLLECTION).find_one(filter, callback=on_results)

    @classmethod
    def save(cls, model):
        '''
        Сохраняет модель в базу.
        @param model: Model
        '''
        data = cls._model_to_dict(model)
        DbClient.get_collection(cls.COLLECTION).save(data)
