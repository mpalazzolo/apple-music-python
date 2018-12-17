from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='apple-music-python',
    url='https://github.com/mpalazzolo/apple-music-python',
    version='1.0.1',
    packages=['applemusicpy'],
    license='LICENSE.txt',
    author='Matt Palazzolo',
    author_email='mattpalazzolo@gmail.com',
    description='A python wrapper for the Apple Music API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.20.1',
        'pyjwt>=1.6.4',
    ],
)
