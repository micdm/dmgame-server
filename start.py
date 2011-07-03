#!../bin/python
# coding=utf8
'''
Скрипт для запуска серверов.
@author: Mic, 2011
'''

from sys import argv

from dmgame.servers import main, policy, web

def start_server(name):
    '''
    Запускает указанный сервер
    @param name: string
    '''
    if argv[1] == 'main':
        main.start_server()
        return
    if argv[1] == 'policy':
        policy.start_server()
        return
    if argv[1] == 'web':
        web.start_server()
        return
    print 'unknown server "%s"'%name


if __name__ == '__main__':
    if len(argv) < 2:
        print 'please specify server to start'
    else:
        start_server(argv[1])
