#!/bin/bash

# Sodium Builder
# - This file will install all the needed packages, pull in AlgLib and install it

# Switch between distributions
if [ -x "$(command -v yum)" ]; then
  # This is a CentOS/RHEL distro
  yum install python2.7 wget git python-pip -y
fi
if [ -x "$(command -v apt)" ]; then
  # This is a Debian/Ubuntu distro
  # Pull in Python3 Virtual Environment packages
  apt-get install python2.7 wget git python-pip -y
fi

pip3 install -r requirements.txt

wget http://www.alglib.net/translator/re/alglib-3.15.0.cpython.free.zip

unzip -o alglib-*.zip

cd cpython && python ./setup.py install

cd .. && rm -rf alglib-*.zip

echo "\n\n"
echo 'Now just run: python ./check.py'
echo 'or'
echo 'python ./xmlrpc-server.py -s'
