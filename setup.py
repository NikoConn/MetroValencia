from setuptools import setup

setup(
    name='MetroValencia',
    version='1.0.2',
    scripts=['./metrovalencia/metrovalencia_cli.py'],
    author='NikoConn',
    description='Api for MetroValencia.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    packages=['metrovalencia'],
    install_requires=[
        'datetime',
        'requests',
        'bs4',
        'pytz'
    ],
    python_requires='>=3.7'
)