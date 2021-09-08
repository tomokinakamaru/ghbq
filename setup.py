from setuptools import find_packages
from setuptools import setup

pkgs = find_packages('src')

name = pkgs[0]

setup(
    entry_points={'console_scripts': [
        f'{name}-generate={name}.generate:main',
        f'{name}-download={name}.download:main',
        f'{name}-sample={name}.sample:main',
        f'{name}-split={name}.split:main'
    ]},
    install_requires=[
        'atomicwrites==1.4.0',
        'progress==1.5',
        'ratelimit==2.2.1'
    ],
    name=name,
    package_dir={'': 'src'},
    packages=pkgs
)
