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
            'id': self.member.number,
            'members': [member.number for member in self.all_members]
        }
        
        
class GameEndedPacket(GamePacket):
    '''
    Игра завершилась.
    '''
    
    type = 'game_ended'


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
        return {'member': self.member.number}
    
    
class MemberLeavingPacket(GamePacket):
    '''
    Игрок выходит из игры.
    '''
    
    type = 'member_leaving'

    def __init__(self, member):
        '''
        @param member: TableMember
        '''
        self.member = member

    def _get_data(self):
        return {'member': self.member.number}
    
    
class ResultsAvailablePacket(GamePacket):
    '''
    Доступны результаты игры.
    '''
    
    type = 'results_available'
    
    def __init__(self, members):
        '''
        @param members: list
        '''
        self.members = members
        
    def _get_data(self):
        return [{'id': member.number, 'result': member.result} for member in self.members]


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
        result = {'member': self.member.number}
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
            info = {'id': member.number, 'cards': cards}
            result.append(info)
        return result
