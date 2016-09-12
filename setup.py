from setuptools import setup
import sys

setup(
    name='GripitModbusMaster',
    version='1.0.0',
    description='GripIt Master',
    url='http://github.com/agilefreaks',
    author='Agilefreaks',
    author_email='agilefreaks@agilefreaks.com',
    license='MIT',
    packages=[
        'gripit',
        'gripit.data',
        'gripit.jobs',
        'gripit.models',
        'gripit.services',
        'gripit.exceptions',
        'gripit.core'
    ],
    install_requires=[
        'pymodbus >= 1.2.0',
    ] + (['RPi.GPIO >= 0.6.2'] if 'posix' in sys.platform else []),
    dependency_links=[
        'http://github.com/Agilefreaks/pymodbus/tarball/' +
        'python3#egg=pymodbus-1.2.0'
    ],
    tests_require=['pytest', 'mock'],
    zip_safe=False
)
