# coding=utf-8
'''
Настройки.
@author: Mic, 2011
'''

from os import getcwd

DEBUG = True

# Директории проекта:
PROJECT_DIR = getcwd()
STATIC_DIR = '%s/static/'%PROJECT_DIR
TEMPLATE_DIR = '%s/templates/'%PROJECT_DIR

# Список модулей, для которых логиование включено.
# Игнорируется, если равно None.
ENABLE_LOGGING_FOR = None

# Описание запускаемых серверов (хост, порт):
SERVERS = {
    'ws': ('game.mic-dm.tom.ru', 8888),
    'web': ('', 8080)
}

# Максимальное количество одновременных подключений:
MAX_CONNECTION_COUNT = 100

try:
    from dmgame.settings_local import *
except ImportError:
    pass
