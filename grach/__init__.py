# -*- coding: utf-8 -*-

'''
init five
'''

from os import environ

if not environ.get('TOKEN'):
    input_data = input('Enter token (\'c\' to cancel): ')
    if input_data == 'c':
        exit(0)
    else:
        environ['TOKEN'] = input_data
