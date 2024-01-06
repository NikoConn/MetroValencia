from setuptools import setup

setup(
    name='MetroValencia',
    version='1.2.0',
    scripts=['./metrovalencia/metrovalencia_cli'],
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
