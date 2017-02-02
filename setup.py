# -*- coding: utf-8 -*-

'''
жми суда шоб было нормально
'''

from setuptools import setup
import src

setup(
    name='grach',
    version=src.__version__,
    description='Telegram Bot',
    author='lisovskey',
    url='https://github.com/lisovskey/grach',
    packages=['src'],
    install_requires=['requests', 'bs4', 'pyTelegramBotAPI'],
    data_files=['config', ['src\\config.py']]
)
