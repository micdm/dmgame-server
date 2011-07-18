# coding=utf8
'''
Штуки для карточных игр.
@author: Mic, 2011
'''

from random import shuffle

from dmgame.db.models.table_member import CardTableMember
from dmgame.modules.game.table import TableManager
import dmgame.packets.outcoming.game as outcoming
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
    
    RANK_ACE = 1
    RANK_TWO = 2
    RANK_SIX = 6
    RANK_JACK = 11
    RANK_QUEEN = RANK_JACK + 1
    RANK_KING = RANK_QUEEN + 1

    def __init__(self, suit, rank):
        '''
        @param suit: string
        @param rank: string
        '''
        self.suit = suit
        self.rank = rank
        
    def _get_rank_as_string(self):
        '''
        Возвращает ранг как строку.
        @return: string
        '''
        ranks = {self.RANK_ACE: 'A', self.RANK_JACK: 'J', self.RANK_QUEEN: 'Q', self.RANK_KING: 'K'}
        if self.rank in ranks:
            return ranks[self.rank]
        return self.rank
        
    def __str__(self):
        return '%s%s'%(self.suit, self._get_rank_as_string())
    
    def is_ace(self):
        '''
        Туз?
        @return: bool
        '''
        return self.rank == self.RANK_ACE
    
    def is_jack(self):
        '''
        Валет?
        @return: bool
        '''
        return self.rank == self.RANK_JACK
    
    def is_queen(self):
        '''
        Дама?
        @return: bool
        '''
        return self.rank == self.RANK_QUEEN
    
    def is_king(self):
        '''
        Король?
        @return: bool
        '''
        return self.rank == self.RANK_KING

    
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
            return CardSet(Card(suit, rank) for rank in [Card.RANK_ACE] + range(Card.RANK_SIX, Card.RANK_KING + 1))
        if type == self.TYPE_52:
            return CardSet(Card(suit, rank) for rank in range(Card.RANK_ACE, Card.RANK_KING + 1))
        
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
    
    
class CardTableManager(TableManager):
    '''
    Абстрактный карточный игровой стол.
    '''

    def __init__(self, *args, **kwargs):
        self._deck = None
        super(CardTableManager, self).__init__(*args, **kwargs)
    
    @classmethod
    def _get_member_class(cls):
        return CardTableMember
    
    @classmethod
    def _get_member_object(cls, *args, **kwargs):
        member = super(CardTableManager, cls)._get_member_object(*args, **kwargs)
        member.hand = MemberHand()
        return member

    def _create_deck(self, type, count):
        '''
        Создает колоду карт с указанными параметрами.
        @param type: string
        @param count: int
        '''
        self._deck = CardDeck(type, count)
        
    def _send_giving_cards_message(self, recipient, cards):
        '''
        Рассылает сообщение о получении игроком карт.
        @param recipient: CardTableMember
        @param cards: CardSet
        '''
        for member in self._model.get_members():
            if member == recipient:
                packet = outcoming.GivingCardsPacket(recipient, cards, True)
            else:
                packet = outcoming.GivingCardsPacket(recipient, cards, False)
            self._send_to_member(member, packet)
        
    def _give_cards_to_member(self, member, count):
        '''
        Выдает карты игроку.
        @param member: CardTableMember
        @param count: int
        '''
        cards = self._deck.get_cards(count)
        logger.debug('giving cards %s to player %s'%(cards, member))
        member.hand.extend(cards)
        self._send_giving_cards_message(member, cards)
        self._on_give_cards_to_member(member, cards)
        
    def _open_all_cards(self):
        '''
        Открывает карты всех игроков.
        '''
        packet = outcoming.OpeningCardsPacket(self._model.get_members())
        self._send_to_all(packet)
        self._on_open_all_cards()
        
    def _on_give_cards_to_member(self, member, cards):
        '''
        Выполняется при выдаче карт игроку.
        @param member: CardTableMember
        @param cards: CardSet
        '''

    def _on_open_all_cards(self):
        '''
        Выполняется при открытии всех карт.
        '''
