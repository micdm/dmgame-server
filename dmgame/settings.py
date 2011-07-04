# coding=utf-8
'''
Настройки.
@author: Mic, 2011
'''

from os import getcwd

DEBUG = True

PROJECT_DIR = getcwd()

SERVERS = {
    'ws': ('game.mic-dm.tom.ru', 8888),
    'web': ('', 8080)
}

STATIC_DIR = '%s/static/'%PROJECT_DIR
TEMPLATE_DIR = '%s/templates/'%PROJECT_DIR
