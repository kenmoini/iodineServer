#!/bin/bash

# Pull in Python3 Virtual Environment packages
sudo apt-get install python3 python3-venv virtualenv wget

# Create a Virtual environment
sudo python3 -m venv venv

# Change context into virtual environment
sudo source venv/bin/activate

sudo pip3 install -r requirements.txt

wget http://www.alglib.net/translator/re/alglib-3.15.0.cpython.free.zip

unzip -o alglib-*.zip

cd cpython && sudo python3 ./setup.py install --prefix=../venv

cd .. && rm -rf cpython && rm -rf alglib-*.zip

sudo python3 ./rest-api.py -s
