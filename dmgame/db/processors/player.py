# coding=utf8
'''
Процессор игроков.
@author: Mic, 2011
'''

from dmgame.db.models import Player
from dmgame.db.processors.base import ModelProcessor
from dmgame.db.processors.user import UserProcessor
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class PlayerProcessor(ModelProcessor):
    '''
    Процессор игроков.
    '''
    
    _model = Player
    _fields = ['connection_id']
    
    @classmethod
    def model_to_dict(cls, model):
        result = super(PlayerProcessor, cls).model_to_dict(model)
        result['user'] = UserProcessor.model_to_dict(model.user)
        return result
