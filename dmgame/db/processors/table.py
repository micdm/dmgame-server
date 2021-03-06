# coding=utf8
'''
Процессор данных об игровых столах.
@author: Mic, 2011
'''

from dmgame.db.models.table import GamblingTable
from dmgame.db.models.table_member import TableMember
from dmgame.db.processors.base import ModelProcessor, DocumentProcessor
from dmgame.db.processors.player import PlayerProcessor

class MemberProcessor(ModelProcessor):
    '''
    Процессор членов стола.
    '''
    
    _model = TableMember
    _fields = ModelProcessor._fields + ['number', 'is_turning_first', 'result']
    
    @classmethod
    def model_to_dict(cls, model):
        result = super(MemberProcessor, cls).model_to_dict(model)
        result['player'] = PlayerProcessor.model_to_dict(model.player)
        return result


class GamblingTableProcessor(DocumentProcessor):
    '''
    Процессор данных об игровых столах.
    '''

    _collection = 'table'
    _model = GamblingTable
    _fields = DocumentProcessor._fields + ['start_time', 'end_time']

    @classmethod
    def model_to_dict(cls, model):
        result = super(GamblingTableProcessor, cls).model_to_dict(model)
        result['members'] = map(MemberProcessor.model_to_dict, model.get_members())
        return result
