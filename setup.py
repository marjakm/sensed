from distutils.core import setup

setup(
    name='Sensed',
    version='0.1.0',
    author='Elmo Trolla',
    author_email='fdfdkz@gmail.com',
    packages=['sensed',],
    scripts=['bin/sensed',],
	url='https://github.com/fdkz/sensed',
    license='LICENSE.txt',
    description='A simple 2D node editor.',
    long_description=open('README.txt').read(),
    install_requires=[
        "PyOpenGL",
        "pysdl2",
		"numpy",
		"nanomsg"
    ],
	dependency_links=['http://github.com/tonysimpson/nanomsg-python/tarball/master#egg=nanomsg',],
)
