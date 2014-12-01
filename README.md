Build dependencies
==================

 * python 2.7
 * zc.buildout
 * gcc-c++ (for libopenzwave compilation)
 * udev-devel (for libopenzwave)
 * python-devel (for python-openzwave cython build)
 * patch
 * mercurial (for python-openzwave checkout)

Docker directory
================

Docker directory contains Dockerfile to build an i386 image.

Currently written for personal use, but may be used as an example to setup an
application environment.

For development
===============

Following commands allows remote access to USB controller
 * on slave machine (with controller plugged in) : sudo socat tcp-l:6543,reuseaddr,fork file:/dev/ttyACM0,nonblock,waitlock=/var/run/ttyACM0.lock
 * on host machine (where virtual tty device is needed) : socat pty,link=/dev/ttyACM0,waitslave tcp:slave:6543
