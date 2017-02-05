# -*- coding: utf-8 -*-

'''
инит пять
'''

from src import __main__

__version__ = '0.1'

try:
    from src.config import TOKEN
except ImportError:
    TOKEN = input('Enter token: ')
    with open('src/config.py', 'w', encoding='utf-8') as config:
        config.write('TOKEN = \'' + TOKEN + '\'\n')
finally:
    __main__.main()
