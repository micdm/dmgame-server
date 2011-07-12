# coding=utf8
'''
Штуки для карточных игр.
@author: Mic, 2011
'''

from random import shuffle

from dmgame.modules.game.table import GamblingTable, TableMember
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Card(object):
    '''
    Карта.
    '''

    SUIT_HEARTS = '♥'
    SUIT_DIAMONDS = '♦'
    SUIT_CLUBS = '♣'
    SUIT_SPADES = '♠'
    
    RANG_TWO = 2
    RANG_SIX = 6
    RANG_JACK = 11
    RANG_QUEEN = RANG_JACK + 1
    RANG_KING = RANG_QUEEN + 1
    RANG_ACE = RANG_KING + 1

    def __init__(self, suit, rang):
        '''
        @param suit: string
        @param rang: string
        '''
        self.suit = suit
        self.rang = rang
        
    def _get_rang_as_string(self):
        '''
        Возвращает ранг как строку.
        @return: string
        '''
        rangs = {self.RANG_JACK: 'J', self.RANG_QUEEN: 'Q', self.RANG_KING: 'K', self.RANG_ACE: 'A'}
        if self.rang in rangs:
            return rangs[self.rang]
        return self.rang
        
    def __str__(self):
        return '%s%s'%(self.suit, self._get_rang_as_string())
    
    def is_jack(self):
        '''
        Валет?
        @return: bool
        '''
        return self.rang == self.RANG_JACK
    
    def is_queen(self):
        '''
        Дама?
        @return: bool
        '''
        return self.rang == self.RANG_QUEEN
    
    def is_king(self):
        '''
        Король?
        @return: bool
        '''
        return self.rang == self.RANG_KING
    
    def is_ace(self):
        '''
        Туз?
        @return: bool
        '''
        return self.rang == self.RANG_ACE
    
    
class CardSet(list):
    '''
    Набор карт.
    Опять же для красивых принтов :).
    '''
    
    def __str__(self):
        return '<%s>'%', '.join(map(str, self))


class CardDeck(object):
    '''
    Колода карт.
    '''
    
    TYPE_36 = '36'
    TYPE_52 = '52'
    
    def __init__(self, type, count):
        '''
        @param type: string
        @param count: int
        '''
        self.cards = self._get_shuffled_cards(type, count)
        
    def _get_cards_with_suit(self, suit, type):
        '''
        Возвращает набор карт одной масти.
        @param suit: string
        @param type: string
        @return: CardSet
        '''
        if type == self.TYPE_36:
            return CardSet(Card(suit, rang) for rang in range(Card.RANG_SIX, Card.RANG_ACE + 1))
        if type == self.TYPE_52:
            return CardSet(Card(suit, rang) for rang in range(Card.RANG_TWO, Card.RANG_ACE + 1))
        
    def _get_one_deck(self, type):
        '''
        Возвращает одну колоду карт.
        @param type: string
        @return: CardSet
        '''
        cards = CardSet()
        for suit in (Card.SUIT_HEARTS, Card.SUIT_DIAMONDS, Card.SUIT_CLUBS, Card.SUIT_SPADES):
            cards += self._get_cards_with_suit(suit, type)
        return cards
    
    def _get_shuffled_cards(self, type, count):
        '''
        Возвращает набор перемешанных карт.
        @param type: string
        @param count: int
        '''
        cards = CardSet()
        for _ in range(count):
            cards += self._get_one_deck(type)
        shuffle(cards)
        return cards
    
    def get_cards(self, count):
        '''
        Выдает указанное количество карт.
        @param count: int
        @return: CardSet
        '''
        cards = CardSet()
        for _ in range(count):
            cards.append(self.cards.pop())
        return cards


class MemberHand(CardSet):
    '''
    Карты игрока.
    '''
    
    
class CardTableMember(TableMember):
    
    def __init__(self, player):
        super(CardTableMember, self).__init__(player)
        self.hand = MemberHand()


class CardGamblingTable(GamblingTable):
    '''
    Абстрактный карточный игровой стол.
    '''

    def __init__(self, *args, **kwargs):
        self._deck = None
        self._hands = {}
        super(CardGamblingTable, self).__init__(*args, **kwargs)
        
    def _get_member_class(self):
        return CardTableMember

    def _create_deck(self, type, count):
        '''
        Создает колоду карт с указанными параметрами.
        @param type: string
        @param count: int
        '''
        self._deck = CardDeck(type, count)
        
    def _give_cards_to_member(self, member, count):
        '''
        Выдает карты игроку.
        @param member: CardTableMember
        @param count: int
        '''
        cards = self._deck.get_cards(count)
        logger.debug('giving cards %s to player %s'%(cards, member))
        member.hand.extend(cards)
        
    def _open_all_cards(self):
        '''
        Открывает карты всех игроков.
        '''
        # TODO: разослать всем событие открыть карты
