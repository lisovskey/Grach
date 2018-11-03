'''
init five
'''

from os import environ

if not environ.get('TOKEN'):
    environ['TOKEN'] = input('Enter token: ')
