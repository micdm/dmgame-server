# coding=utf8

from dmgame.db.models.table_member import CardTableMember

class TableMember(CardTableMember):
    
    def _get_card_value(self, card):
        '''
        Возвращает вес карты.
        @param card: Card
        @return: int
        '''
        if card.is_ace():
            return 1
        if card.is_jack():
            return 2
        if card.is_queen():
            return 3
        if card.is_king():
            return 4
        return card.rank

    def get_hand_value(self):
        '''
        Подсчитывает сумму карт в руке.
        @return: int
        '''
        return sum(self._get_card_value(card) for card in self.hand)
