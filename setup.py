# -*- coding: utf-8 -*-

'''
жми суда шоб было нормально
'''

from setuptools import setup

def get_requirements():
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
    version='0.2',
    description='Telegram Bot',
    author='lisovskey',
    author_email='ritofzeed@gmail.com',
    include_package_data=True,
    license='MIT',
    url='https://github.com/lisovskey/grach',
    packages=['grach'],
    install_requires=get_requirements()
)
