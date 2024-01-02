from setuptools import setup

setup(
    name='MetroValencia',
    version='1.0',
    scripts=['./metrovalencia/metrovalencia_cli.py'],
    author='NikoConn',
    description='Api for MetroValencia.',
    packages=['metrovalencia'],
    install_requires=[
        'datetime',
        'requests',
        'bs4',
        'pytz'
    ],
    python_requires='>=3.7'
)