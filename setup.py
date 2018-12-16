from setuptools import setup

setup(
    name='apple-music-python',
    version='1.0.0',
    packages=['applemusicpy'],
    url='',
    license='LICENSE.txt',
    author='Matt Palazzolo',
    author_email='mattpalazzolo@gmail.com',
    description='A python wrapper for the Apple Music API',
    install_requires=[
        'requests>=2.18.4',
        'jwt>=0.5.4',
    ],
)