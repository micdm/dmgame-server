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
    def model_to_dict(cls, model):
        result = super(DocumentProcessor, cls).model_to_dict(model)
        if hasattr(model, '_id'):
            result['_id'] = model._id
        return result

    @classmethod
    def dict_to_model(cls, dict):
        model = super(DocumentProcessor, cls).dict_to_model(dict)
        model._id = dict['_id']
        return model

    @classmethod
    def find(cls, filter):
        '''
        Ищет записи.
        @param filter: dict
        @return: list
        '''
        data = DbClient.get_collection(cls._collection).find(filter)
        return map(cls.dict_to_model, data)
    
    @classmethod
    def find_one(cls, filter):
        '''
        Ищет одну запись.
        @param filter: dict
        @return: Model
        '''
        data = DbClient.get_collection(cls._collection).find_one(filter)
        if data is None:
            return None
        return cls.dict_to_model(data)

    @classmethod
    def save(cls, model):
        '''
        Сохраняет модель в базу.
        @param model: Model
        '''
        data = cls.model_to_dict(model)
        model._id = DbClient.get_collection(cls._collection).save(data, manipulate=True)
