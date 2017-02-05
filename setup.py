# -*- coding: utf-8 -*-

'''
жми суда шоб было нормально
'''

from setuptools import setup
import src

def requirements():
    '''
    устанавливаю все
    '''
    requirements_list = []

    with open('requirements.txt') as reqs:
        for install in reqs:
            requirements_list.append(install.strip())

    return requirements_list

setup(
    name='grach',
    version=src.__version__,
    description='Telegram Bot',
    author='lisovskey',
    license='MIT',
    url='https://github.com/lisovskey/grach',
    packages=['src'],
    install_requires=requirements(),
    data_files=['config', ['src\\config.py']]
)
