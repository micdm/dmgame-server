# coding=utf8
'''
Реализация игры, похожей на "21".
Карты сдаются двум игрокам. Игрок может либо взять карту, либо остановиться
и передать ход другому. Выигрывает тот, кто наберет сумму очков наиболее близкую к 21.
@author: Mic, 2011
'''

from dmgame.modules.game.cards import CardDeck, CardGamblingTable
import dmgame.modules.game.errors as errors
from dmgame.modules.game.table import PlayerTurn
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class OneMoreCardTurn(PlayerTurn):
    '''
    Нужна еще одна карта.
    '''

    
class CardsEnoughTurn(PlayerTurn):
    '''
    Карт достаточно.
    '''


class GamblingTable(CardGamblingTable):

    MAX_SUM = 21

    def _get_hand_sum(self, hand):
        '''
        Подсчитывает сумму карт в руке.
        @param hand: PlayerHand
        @return: int
        '''
        sum = 0
        for card in hand:
            # TODO: посчитать сумму
            pass
        return sum

    def _get_turn_object(self, turn_data):
        if 'type' not in turn_data:
            raise errors.BadTurnDataError('turn data must contain "type" field')
        turn_type = turn_data['type']
        if turn_type == 'one_more_card':
            return OneMoreCardTurn(turn_data)
        if turn_type == 'cards_enough':
            return CardsEnoughTurn(turn_data)
        raise errors.BadTurnDataError('unknown turn type "%s"'%turn_type)

    def _on_start(self):
        '''
        На старте раздаем по две карты и передаем ход произвольному игроку.
        '''
        self._create_deck(CardDeck.TYPE_36, 1)
        for member in self._members.values():
            self._give_cards_to_member(member, 2)
        self._set_random_member_turning()
        
    def _on_end(self):
        '''
        В конце игры показываем карты, вычисляем победителей и проигравших.
        '''
        self._open_all_cards()
        # TODO: вычислить победителей

    def _on_member_turn(self, member, turn):
        '''
        Игрок может либо запросить карту, либо остановиться.
        '''
        if isinstance(turn, OneMoreCardTurn):
            self._give_cards_to_member(member, 1)
            sum = self._get_hand_sum(member.hand)
            if sum > self.MAX_SUM:
                self._end()
        if isinstance(turn, CardsEnoughTurn):
            if member.is_first_turning:
                self._set_next_member_turning()
            else:
                self._end()

    def _on_member_leave(self, member_left):
        '''
        Если один игрок уходит, делаем второго победителем и заканчиваем игру.
        '''
        for member in self._members.values():
            if member_left == member:
                self._set_member_result(member, self.PLAYER_RESULT_DEFEAT)
            else:
                self._set_member_result(member, self.PLAYER_RESULT_WIN)
        self._end()
