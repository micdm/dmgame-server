# coding=utf8
'''
Исходящие Game-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.outcoming import OutcomingPacket

class GamePacket(OutcomingPacket):
    '''
    Базовый абстрактный класс.
    '''

    namespace = 'game'


class GameStartedPacket(GamePacket):
    '''
    Игра началась.
    '''
    
    type = 'game_started'

    def __init__(self, member, all_members):
        '''
        @param member: TableMember
        @param all_members: list
        '''
        self.member = member
        self.all_members = all_members

    def _get_data(self):
        return {
            'id': self.member.player.connection_id,
            'members': [member.player.connection_id for member in self.all_members]
        }


class MemberTurningPacket(GamePacket):
    '''
    Ход переходит к указанному игроку.
    '''
    
    type = 'member_turning'

    def __init__(self, member):
        '''
        @param member: TableMember
        '''
        self.member = member

    def _get_data(self):
        return {'member': self.member.player.connection_id}


class GivingCardsPacket(GamePacket):
    '''
    Выдача карт игроку.
    '''
    
    type = 'giving_cards'
    
    def __init__(self, member, cards=None, count=None):
        '''
        @param member: TableMember
        @param cards: CardSet
        @param count: int
        '''
        self.member = member
        self.cards = cards
        self.count = count
        
    def _get_data(self):
        result = {'member': self.member.player.connection_id}
        if self.cards is not None:
            result['cards'] = [card.as_dict() for card in self.cards]
        if self.count is not None:
            result['count'] = self.count
        return result
    
    
class OpeningCardsPacket(GamePacket):
    '''
    Раскрытие карт всех игроков.
    '''
    
    type = 'opening_cards'
    
    def __init__(self, members):
        '''
        @param members: list
        '''
        self.members = members
        
    def _get_data(self):
        result = []
        for member in self.members:
            cards = [card.as_dict() for card in member.hand]
            info = {'id': member.player.connection_id, 'cards': cards}
            result.append(info)
        return result
