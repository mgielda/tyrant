from setuptools import setup, find_packages

setup(
    name = 'tyrant',
    version = '0.1',
    packages = ['tyrant'],
    install_requires = ['argh','sarge','watchdog'],
)
