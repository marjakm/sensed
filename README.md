sensed
======

A simple 2D node editor. Experimenting with wireless sensor network editing/visualization. Just a quick timewaste..

install with pip >= 1.5:
pip install --process-dependency-links git+https://github.com/fdkz/sensed


prerequisites
=============

pip install PyOpenGL
pip install pysdl2
pip install numpy
pip install cython ?
pip install git+https://github.com/tonysimpson/nanomsg-python.git

nanomsg:
    sudo apt-get install checkinstall

    mkdir build
    cd build
    wget http://download.nanomsg.org/nanomsg-0.3-beta.tar.gz
    tar xvzf nanomsg-0.3-beta.tar.gz
    cd nanomsg-0.3-beta
    ./configure --prefix=/usr
    make
    make check

    sudo checkinstall --pkgname=nanomsg --pkgversion=0.3-beta --pkgrelease=1 --maintainer=admin@example.com --install=no -D -y make install

    dpkg --contents nanomsg_0.3-beta-1_amd64.deb
    sudo dpkg -i nanomsg_0.3-beta-1_amd64.deb


linux:
    sudo apt-get install libglu1-mesa-dev freeglut3-dev mesa-common-dev ?

installing ctypes under windows:
    install Visual Studio 2012 (win7/win8/win8.1)
    SET VS90COMNTOOLS=%VS110COMNTOOLS%
    pip install cython

download libsdl2
http://www.libsdl.org/download-2.0.php
