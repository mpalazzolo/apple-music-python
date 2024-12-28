from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='apple-music-python',
    url='https://github.com/j-jacobson/apple-music-python',
    version='2.0.0',
    packages=['applemusicpy'],
    license='LICENSE.txt',
    author='Matt Palazzolo, Jonathan Jacobson',
    author_email='mattpalazzolo@gmail.com, jonjacobson715@gmail.com',
    description='A python wrapper for the Apple Music API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests>=2.21',
        'pyjwt>=1.7.1',
        'cryptography>=3.2'
    ],
)
