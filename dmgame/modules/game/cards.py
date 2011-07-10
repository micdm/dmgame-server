# coding=utf8
'''
Штуки для карточных игр.
@author: Mic, 2011
'''

from random import shuffle

from dmgame.modules.game.table import GamblingTable
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
        if self.rang == 13:
            return 'A'
        if self.rang == 12:
            return 'K'
        if self.rang == 11:
            return 'Q'
        if self.rang == 10:
            return 'J'
        return self.rang
        
    def __str__(self):
        return '%s%s'%(self.suit, self._get_rang_as_string())
    
    
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
            return CardSet(Card(suit, rang) for rang in range(6, 14))
        if type == self.TYPE_52:
            return CardSet(Card(suit, rang) for rang in range(2, 14))
        
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


class PlayerHand(object):
    '''
    Карты игрока.
    '''
    
    def __init__(self):
        '''
        @param cards: list
        '''
        self._cards = []

    def add_cards(self, cards):
        '''
        Добавляет карты в руку.
        @param cards: CardSet
        '''
        self._cards.extend(cards)


class CardGamblingTable(GamblingTable):
    '''
    Абстрактный карточный игровой стол.
    '''

    def __init__(self, *args, **kwargs):
        self._deck = None
        self._hands = {}
        super(CardGamblingTable, self).__init__(*args, **kwargs)

    def _create_deck(self, type, count):
        '''
        Создает колоду карт с указанными параметрами.
        @param type: string
        @param count: int
        '''
        self._deck = CardDeck(type, count)
        
    def _give_cards_to_player(self, player, count):
        '''
        Выдает карты игроку.
        @param player: Player
        @param count: int
        '''
        if player not in self._hands:
            self._hands[player] = PlayerHand()
        cards = self._deck.get_cards(count)
        logger.debug('giving cards %s to player %s'%(cards, player))
        self._hands[player].add_cards(cards)
