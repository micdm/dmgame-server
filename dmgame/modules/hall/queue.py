# coding=utf8
'''
Очередь на вход в игру.
@author: Mic, 2011
'''

from dmgame.modules.game.player import PlayersParty

class PlayersQueue(object):
    '''
    Очередь игроков.
    '''
    
    PARTY_SIZE = 2
    
    def __init__(self):
        self._queue = []
        
    def has_player(self, player):
        '''
        Возвращает, есть ли игрок в очереди.
        @param player: Player
        @return: bool
        '''
        return player in self._queue
    
    def add_player(self, player):
        '''
        Добавляет в очередь игрока.
        @param player: Player
        '''
        self._queue.append(player)
        
    def remove_party(self, party):
        '''
        Удаляет из очереди игроков группы.
        @param party: PlayersParty
        '''
        for player in party.players:
            self._queue.remove(player)
        
    def find_party_for_last_player(self):
        '''
        Находит компанию для последнего игрока в очереди.
        @return: PlayersParty
        '''
        last = self._queue[-1]
        if len(self._queue) >= self.PARTY_SIZE:
            count = self.PARTY_SIZE - 1
            return PlayersParty(self._queue[:count] + [last])
        return None
