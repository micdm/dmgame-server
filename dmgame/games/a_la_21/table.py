# coding=utf8
'''
Реализация игры, похожей на "21".
Карты сдаются двум игрокам. Игрок может либо взять карту, либо остановиться
и передать ход другому. Выигрывает тот, кто наберет сумму очков наиболее близкую к 21.
@author: Mic, 2011
'''

import dmgame.games.a_la_21.outcoming as outcoming
from dmgame.modules.game.cards import CardDeck, CardGamblingTable, TableMember as BaseTableMember
from dmgame.modules.game.table import PlayerTurn
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class TableMember(BaseTableMember):
    
    def _get_card_value(self, card):
        '''
        Возвращает вес карты.
        @param card: Card
        @return: int
        '''
        if card.is_jack():
            return 2
        if card.is_queen():
            return 3
        if card.is_king():
            return 4
        if card.is_ace():
            return 11
        return card.rank

    def get_hand_value(self):
        '''
        Подсчитывает сумму карт в руке.
        @return: int
        '''
        return sum(self._get_card_value(card) for card in self.hand)


class OneMoreCardTurn(PlayerTurn):
    '''
    Нужна еще одна карта.
    '''

    
class CardsEnoughTurn(PlayerTurn):
    '''
    Карт достаточно.
    '''


class GamblingTable(CardGamblingTable):

    MAX_VALUE = 21
    
    def _get_member_class(self):
        return TableMember

    def _get_turn_class(self, turn_type):
        if turn_type == 'one_more_card':
            return OneMoreCardTurn
        if turn_type == 'cards_enough':
            return CardsEnoughTurn
        return None
    
    def _get_max_value(self):
        '''
        Возвращает максимальную сумму для всех игроков (без перебора).
        @return: int
        '''
        max_value = 0
        for member in self._members.values():
            value = member.get_hand_value()
            if value <= self.MAX_VALUE and max_value < value:
                max_value = value
        return max_value
    
    def _get_member_result(self, max_value, member):
        '''
        Возвращает результат игрока.
        @param max_value: int
        @param member: TableMember
        '''
        value = member.get_hand_value()
        logger.debug('member %s has value %s for hand %s'%(member, value, member.hand))
        if value == max_value:
            return self._results.RESULT_WIN
        return self._results.RESULT_DEFEAT

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
        max_value = self._get_max_value()
        for member in self._members.values():
            result = self._get_member_result(max_value, member)
            self._results.set_member_result(member, result)

    def _on_member_turn(self, member, turn):
        '''
        Игрок может либо запросить карту, либо остановиться.
        '''
        if isinstance(turn, OneMoreCardTurn):
            self._give_cards_to_member(member, 1)
            sum = self._get_hand_sum(member.hand)
            if sum >= self.MAX_VALUE:
                self._end()
        if isinstance(turn, CardsEnoughTurn):
            if member.is_turning_first:
                self._set_next_member_turning()
            else:
                self._end()

    def _on_member_leave(self, member_left):
        '''
        Если один игрок уходит, заканчиваем игру.
        '''
        self._end()
        
    def _on_give_cards_to_member(self, member, cards):
        '''
        При выдаче карт игроку шлем сумму всех его карт.
        '''
        packet = outcoming.SetHandValuePacket(member, member.get_hand_value())
        self._send_to_member(member, packet)
        
    def _on_open_all_cards(self):
        '''
        При вскрытии карт рассылаем всем суммы карт других игроков.
        '''
        for member in self._members.values():
            packet = outcoming.SetHandValuePacket(member, member.get_hand_value())
            self._send_to_all(packet)
