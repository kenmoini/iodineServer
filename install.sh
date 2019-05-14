#!/bin/bash

# Sodium Builder
# - This file will install all the needed packages, pull in AlgLib and install it

# Switch between distributions
if [ -x "$(command -v yum)" ]; then
  # This is a CentOS/RHEL distro
  yum install python3 wget git python3-pip -y
fi
if [ -x "$(command -v apt)" ]; then
  # This is a Debian/Ubuntu distro
  # Pull in Python3 Virtual Environment packages
  apt-get install python3 wget git python3-pip -y
fi

pip3 install -r requirements.txt

wget http://www.alglib.net/translator/re/alglib-3.15.0.cpython.free.zip

unzip -o alglib-*.zip

cd cpython && python3 ./setup.py install

cd .. && rm -rf cpython && rm -rf alglib-*.zip

echo 'Now just run: python3 ./rest-api.py -s'
