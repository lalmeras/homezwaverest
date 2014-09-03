from setuptools import setup, find_packages

setup(
    name = "homezwaverest",
    version = "1.0",
    license = 'MIT',
    description = "Home Zwave rest server.",
    author = 'Laurent Almeras',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools', 'cornice', 'waitress', 'pyramid_debugtoolbar', 'louie', 'colander >= 1.0b1'],
    entry_points={
        'console_scripts': [
            'runserver = homezwaverest.server:main',
        ],
        'paste.app_factory' : [ 'main = homezwaverest.cornice_server:main' ]
    }
)

