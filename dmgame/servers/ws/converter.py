# coding=utf8
'''
Сериализация/десериализация пакетов.
@author: Mic, 2011
'''
from tornado.escape import json_decode, json_encode

from dmgame.packets import incoming
from dmgame.utils.log import get_logger
logger = get_logger(__name__)

class Converter(object):
    '''
    Класс сериализации/десериализации сообщений.
    '''
    @classmethod
    def serialize(cls, packet):
        '''
        Превращает пакет в текст.
        @param message: dmgame.packets.outcoming.OutcomingPacket
        @return: string
        '''
        try:
            return json_encode(packet.get_dict())
        except:
            logger.debug('can not serialize packet to text')
            return None
    
    @classmethod
    def _check_packet_data(cls, data):
        '''
        Проверяет корректность данных пакета.
        @param data: dict
        '''
        if 'code' not in data or not data['code']:
            raise Exception('packet data must contain non-empty "code" field')
        if len(data['code'].split(':')) != 2:
            raise Exception('packet code has bad format')
        
    @classmethod
    def _build_packet(cls, data):
        '''
        Создает пакет по набору данных.
        @param data: dict
        '''
        code = data['code']
        logger.debug('building packet "%s"'%code)
        namespace, type = code.split(':')
        packet_class = incoming.get_packet_class(namespace, type)
        if packet_class is None:
            logger.debug('packet class for "%s:%s" not found'%(namespace, type))
            return None
        packet = packet_class()
        packet.set_data(data.get('data'))
        logger.debug('packet %s builded'%packet)
        return packet

    @classmethod
    def unserialize(cls, text):
        '''
        Преобразовывает текст в пакет.
        @param text: string
        @return: dmgame.packets.incoming.IncomingPacket
        '''
        try:
            data = json_decode(text)
            cls._check_packet_data(data)
            return cls._build_packet(data)
        except Exception as e:
            logger.debug('can not unserialize text to packet: %s'%e)
            return None
