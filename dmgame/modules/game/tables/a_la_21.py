# coding=utf8
'''
Реализация игры, похожей на "21".
Карты сдаются двум игрокам. Игрок может либо взять карту, либо остановиться
и передать ход другому. Выигрывает тот, кто наберет сумму очков наиболее близкую к 21.
@author: Mic, 2011
'''

from dmgame.modules.game.table import GamblingTable as BaseGamblingTable
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class GamblingTable(BaseGamblingTable):
    '''
    Игровой стол.
    '''
