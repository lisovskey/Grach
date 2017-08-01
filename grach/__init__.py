# -*- coding: utf-8 -*-

'''
инит пять
'''

from os import path, getcwd

try:
    from .config import TOKEN
except ImportError:
    print('Token not found')
    TOKEN = input('Enter token (\'c\' to cancel): ')
    if TOKEN != 'c':
        __location__ = path.join(getcwd(), path.dirname(__file__))
        with open(path.join(__location__, 'config.py'), 'w', encoding='utf-8') as config:
            config.write('TOKEN = \'' + TOKEN + '\'\n')
        print('Token has been saved, start program again')
    exit(0)
