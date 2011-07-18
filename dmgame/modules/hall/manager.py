# coding=utf8
'''
Менджер игрового зала.
@author: Mic, 2011
'''

from dmgame.db.models.player import Player
from dmgame.messages.dispatcher import player_dispatcher, user_dispatcher
import dmgame.messages.messages as messages
from dmgame.modules.hall.queue import PlayersQueue
import dmgame.packets.incoming.hall as incoming
import dmgame.packets.outcoming.hall as outcoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class MessageResender(object):
    '''
    Пересыльщик сообщений на новый уровень - от пользователя к игроку.
    '''
    
    def __init__(self):
        self._players = {}
        self._subscribe()

    def _get_player(self, user, connection_id):
        '''
        Ищет игрока в коллекции. Если его там нет, создает нового и добавляет.
        @param user: User
        @param connection_id: int
        @return: Player
        '''
        if connection_id in self._players:
            player = self._players[connection_id]
        else:
            player = Player(user, connection_id)
            self._players[connection_id] = player
        return player

    def _on_user_request(self, message):
        '''
        Рассылает сообщение, что от игрока получен запрос.
        @param message: UserRequestMessage
        '''
        logger.debug('sending player request message')
        player = self._get_player(message.user, message.connection_id)
        new_message = messages.PlayerRequestMessage(player, message.packet)
        player_dispatcher.dispatch(new_message)
        
    def _on_user_disconnected(self, message):
        '''
        Рассылает сообщение, что игрок отключился.
        @param message: UserDisconnectedMessage
        '''
        logger.debug('sending player disconnected message')
        player = self._get_player(message.user, message.connection_id)
        new_message = messages.PlayerDisconnectedMessage(player)
        player_dispatcher.dispatch(new_message)
        del self._players[player.connection_id]
        
    def _on_player_response(self, message):
        '''
        Рассылает сообщение, что пользователь получает ответ.
        @param message: PlayerResponseMessage
        '''
        logger.debug('sending user response message')
        player = message.player
        new_message = messages.UserResponseMessage(player.user, player.connection_id, message.packet)
        user_dispatcher.dispatch(new_message)
        
    def _subscribe(self):
        '''
        Подписывается на сообщения.
        '''
        user_dispatcher.subscribe(messages.UserRequestMessage, self._on_user_request)
        user_dispatcher.subscribe(messages.UserDisconnectedMessage, self._on_user_disconnected)
        player_dispatcher.subscribe(messages.PlayerResponseMessage, self._on_player_response)


class HallManager(object):
    '''
    Игровой зал.
    '''

    def __init__(self):
        self._players_queue = PlayersQueue()
        self._message_resender = MessageResender()
        
    def _can_player_enter(self, player):
        '''
        Может ли игрок войти в игровой зал?
        @param player: Player
        @return: bool
        '''
        return not player.is_in_party and not player.is_in_game

    def _on_player_enter_request(self, message):
        '''
        Выполняется при запросе пользователя на вход в зал.
        @param message: EnterPacket
        '''
        player = message.player
        if self._can_player_enter(player):
            logger.debug('handling hall enter request for player %s'%player)
            packet = outcoming.WelcomePacket()
            message = messages.PlayerResponseMessage(player, packet)
            player_dispatcher.dispatch(message)
        else:
            logger.debug('hall enter request rejected for player %s'%player)

    def _add_to_queue(self, player):
        '''
        Добавляет игрока в очередь.
        @param player: Player
        '''
        if self._players_queue.has_player(player):
            logger.debug('player already in queue')
            return
        logger.debug('adding to players queue')
        self._players_queue.add_player(player)
        party = self._players_queue.find_party_for_last_player()
        if party is None:
            logger.debug('no party yet')
        else:
            logger.debug('party %s found, removing party from queue and sending invites'%party)
            self._players_queue.remove_party(party)
            party.invite()

    def _on_player_play_request(self, message):
        '''
        Выполняется при запросе пользователя на игру.
        @param message: PlayPacket
        '''
        player = message.player
        if self._can_player_enter(player):
            logger.debug('handling hall play request')
            self._add_to_queue(message.player)
        else:
            logger.debug('play request rejected for player %s'%player)
        
    def _subscribe(self):
        '''
        Подписывается на всякие сообщения.
        '''
        player_dispatcher.subscribe_for_packet(incoming.EnterPacket, self._on_player_enter_request)
        player_dispatcher.subscribe_for_packet(incoming.PlayPacket, self._on_player_play_request)

    def init(self):
        '''
        Инициализация.
        '''
        logger.info('initializing hall manager')
        self._subscribe()
