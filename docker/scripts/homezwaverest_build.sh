#! /bin/bash

set -e

#export http_proxy=http://192.168.0.42:8123

useradd homezwaverest
cd /home/homezwaverest
git clone http://github.com/lalmeras/homezwaverest.git
virtualenv --no-site-packages /home/homezwaverest/env
/home/homezwaverest/env/bin/pip install zc.buildout
cd /home/homezwaverest/homezwaverest/buildout
linux32 /home/homezwaverest/env/bin/buildout
yum clean all

