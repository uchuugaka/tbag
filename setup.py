# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name='tbag',
    version='1.1.6',

    packages=['tbag',
              'tbag.core',
              'tbag.core.db',
              'tbag.utils',
              'tbag.utils.error',
              ],

    description='A Tornado tools bag.',

    url='https://github.com/Demon-Hunter/tbag',

    author='huangtao',
    author_email='huangtao@klicen.com',

    license='MIT',
    keywords=['Tornado', 'tools'],

    install_requires=[
        'motor==1.1',
        'tornado==4.5.2',
        'Tornado-MySQL==0.5.1',
    ],
)
