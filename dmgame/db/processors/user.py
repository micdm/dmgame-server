# coding=utf8
'''
Процессор данных о пользователях.
@author: Mic, 2011
'''

from hashlib import sha1

from dmgame.db.models.user import User
from dmgame.db.processors.base import DocumentProcessor
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class UserProcessor(DocumentProcessor):
    '''
    Процессор данных о пользователях.
    '''

    _model = User
    _fields = DocumentProcessor._fields + ['login']
    _collection = 'user'

    @classmethod
    def get_by_login_and_password(cls, login, password):
        '''
        Ищет модель пользователя по логину и паролю.
        Если пользователь не нашелся, возвращает None.
        @param login: string
        @param password: string
        @return: User
        '''
        password_hash = sha1(password).hexdigest()
        filter = {'login': login, 'password_hash': password_hash}
        return cls.find_one(filter)
