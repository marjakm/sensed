from distutils.core import setup

setup(
    name='Sensed',
    version='0.1.0',
    author='Elmo Trolla',
    author_email='fdfdkz@gmail.com',
    packages=['sensed', 'sensed.system', 'sensed.conf', 'sensed.system.modules'],
    package_data={'sensed': ['data/*', 'log/*'], 'sensed.system.modules': ['*/*'] },
    scripts=['bin/sensed',],
    url='https://github.com/fdkz/sensed',
    license='LICENSE.txt',
    description='A simple 2D node editor.',
    long_description=open('README.md').read(),
    install_requires=[
        "nanomsg>=1.0a2",
        "PyOpenGL",
        "pysdl2",
        "numpy",
    ],
    dependency_links=['https://github.com/tonysimpson/nanomsg-python/tarball/master#egg=nanomsg-1.0a2',],
)
