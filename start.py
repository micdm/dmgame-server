#!../bin/python
# coding=utf8
'''
Скрипт для запуска серверов.
@author: Mic, 2011
'''

from sys import argv

from dmgame.servers import policy, web, ws

def start_server(name):
    '''
    Запускает указанный сервер
    @param name: string
    '''
    servers = {
        'policy': policy.start_server,
        'web': web.start_server,
        'ws': ws.start_server
    }
    if name in servers:
        servers[name]()
    else:
        print 'unknown server "%s"'%name


if __name__ == '__main__':
    if len(argv) < 2:
        print 'please specify server to start'
    else:
        start_server(argv[1])
