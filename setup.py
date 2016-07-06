from setuptools import setup

setup(
	name='GripitModbusMasterAsync',
    version='1.0',
    description='GripIt Master Async Version',
    url='http://github.com/agilefreaks',
    author='Agilefreaks',
    author_email='agilefreaks@agilefreaks.com',
    license='MIT',
    packages=['gripit-modbus-master-async'],
	install_requires=[
		'python3'
	],
	dependency_links=[
		'http://github.com/Agilefreaks/pymodbus/tarball/python3'
	],
    zip_safe=False
)