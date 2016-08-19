from setuptools import setup, find_packages

setup(
    name='mempass',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'SQLAlchemy',
        #'PyQt5',
    ],
    entry_points='''
        [console_scripts]
        mempass=mempass.cli:main
        chbs=mempass.correcthorse:cli
        simple=mempass.simple:cli
    ''',
)
