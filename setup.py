from setuptools import setup

setup(
    name='Kwiz Kreator',
    version='1.0',
    description='A tool for creating Trail Trivia files',
    author='John Need',
    author_email='john.need@inulabs.tech',
    packages=['kwiz_kreator'],
    install_requires=[
        'PyQt5',
        'PyQt5-Qt5',
        'PyQt5-sip',
    ]
)