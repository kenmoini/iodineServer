#!/bin/bash

# Sodium Builder
# - This file will install all the needed packages, pull in AlgLib and install it

# Switch between distributions

echo ""
echo "//=========================================================="
echo "  Installing system packages..."
echo "//=========================================================="
if [ -x "$(command -v yum)" ]; then
  # This is a CentOS/RHEL distro
  yum install python2.7 wget python-pip supervisor -y
fi
if [ -x "$(command -v apt)" ]; then
  # This is a Debian/Ubuntu distro
  # Pull in Python3 Virtual Environment packages
  apt-get install python2.7 wget python-pip supervisor -y
fi

echo ""
echo "//=========================================================="
echo "  Creating directories if needed..."
echo "//=========================================================="
mkdir -p /etc/supervisor/conf.d/
mkdir -p /var/run/iodineServer/
chown iodine:iodine /var/run/iodineServer/
chmod 775 /var/run/iodineServer/

echo ""
echo "//=========================================================="
echo "  Installing pip modules..."
echo "//=========================================================="
pip install -r requirements.txt

echo ""
echo "//=========================================================="
echo "  Getting AlgLib 3.15 CPython Library..."
echo "//=========================================================="
wget http://www.alglib.net/translator/re/alglib-3.16.0.cpython.free.zip

echo ""
echo "//=========================================================="
echo "  Unzip AlgLib..."
echo "//=========================================================="
unzip -o alglib-*.zip

echo ""
echo "//=========================================================="
echo "  Installing AlgLib..."
echo "//=========================================================="
cd cpython && python ./setup.py install

echo ""
echo "//=========================================================="
echo "  Clean-up after downloads..."
echo "//=========================================================="
cd .. && rm -rf alglib-*.zip

echo "//=========================================================="
echo "  Starting server for tests... python ./xmlrpc-server.py-s"
echo "//=========================================================="
python ./xmlrpc-server.py -s
echo ""
echo "//=========================================================="
echo "  Running tests..."
echo "//=========================================================="
python ./check.py
echo ""
echo "//=========================================================="
echo "  Stopping server for tests... python ./check.py"
echo "//=========================================================="
python ./xmlrpc-server.py -k
echo ""
echo "//=========================================================="
echo 'Now just run: python ./xmlrpc-server.py -s'
echo 'or'
echo 'python ./check.py'
