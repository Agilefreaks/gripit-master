from setuptools import setup

setup(
	name='GripitModbusMaster',
    version='1.0.0',
    description='GripIt Master',
    url='http://github.com/agilefreaks',
    author='Agilefreaks',
    author_email='agilefreaks@agilefreaks.com',
    license='MIT',
    packages=['gripit-modbus-master'],
	install_requires=[
		'RPi.GPIO >= 0.6.2',
		'pymodbus >= 1.2.0'
	],
	dependency_links=[
		'http://github.com/Agilefreaks/pymodbus/tarball/python3#egg=pymodbus-1.2.0'
	],
    zip_safe=False
)