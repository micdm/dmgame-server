# coding=utf8
'''
Реализация игры, похожей на "21".
Карты сдаются двум игрокам. Игрок может либо взять карту, либо остановиться
и передать ход другому. Выигрывает тот, кто наберет сумму очков наиболее близкую к 21.
@author: Mic, 2011
'''

from dmgame.modules.game.cards import CardDeck, CardGamblingTable
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class GamblingTable(CardGamblingTable):
    '''
    Игровой стол.
    '''

    def _on_start(self):
        '''
        На старте раздаем по две карты и передаем ход произвольному игроку.
        '''
        self._create_deck(CardDeck.TYPE_36, 1)
        for player in self._party.players:
            self._give_cards_to_player(player, 2)
        self._set_random_player_turning()

    def _on_player_turn(self, player, turn):
        '''
        Игрок может либо запросить карту, либо остановиться.
        '''

    def _on_player_leave(self, leaver):
        '''
        Если один игрок уходит, делаем второго победителем и заканчиваем игру.
        @param leaver: Player
        '''
        for player in self._party.players:
            if player == leaver:
                self._set_player_result(player, self.PLAYER_RESULT_DEFEAT)
            else:
                self._set_player_result(player, self.PLAYER_RESULT_WIN)
        self._end()
