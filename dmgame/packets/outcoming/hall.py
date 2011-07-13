# coding=utf8
'''
Исходящие Hall-пакеты.
@author: Mic, 2011
'''

from dmgame.packets.outcoming import OutcomingPacket

def player_as_dict(player):
    '''
    Превращает объект игрока в словарь. 
    @param player: Player
    @return: dict
    '''
    return {'id': player.user.id}


class HallPacket(OutcomingPacket):
    '''
    Игровой зал.
    '''

    namespace = 'hall'


class WelcomePacket(HallPacket):
    '''
    Добро пожаловать в игровой зал.
    '''

    type = 'welcome'

    def _get_data(self):
        '''
        Тут будет информация о зале - количество участников, доступные столы,
        прочая игровая информация. 
        '''


class PartyInvitePacket(HallPacket):
    '''
    Приглашение начать игру.
    '''

    type = 'party_invite'
    
    def __init__(self, dismiss_time):
        '''
        @param dismiss_time: int
        '''
        self.dismiss_time = dismiss_time
        
    def _get_data(self):
        return {'dismiss_time': self.dismiss_time}


class PartyMemberReadyPacket(HallPacket):
    '''
    Еще один участник группы готов начать игру.
    '''
    
    type = 'party_member_ready'
    
    def __init__(self, players, ready_players):
        '''
        @param players: list
        @param ready_players: list
        '''
        self.players = players
        self.ready_players = ready_players

    def _get_data(self):
        ready = []
        non_ready = []
        for player in self.players:
            if player in self.ready_players:
                ready.append(player_as_dict(player))
            else:
                non_ready.append(player_as_dict(player))
        return {'ready': ready, 'non_ready': non_ready}
    
    
class PartyDismissPacket(HallPacket):
    '''
    Группа распущена.
    '''
    
    type = 'party_dismiss'
