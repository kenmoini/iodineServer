# iodineServer
Iodine - An application that serves the computation needs of Salt Smarts

## Introduction
Iodine is the name of the server application that processes fertilizer computation formulae sent from the Salt Smarts platform.

It is a simple XML RPC server written in Python that extends the CPython build of the AlgLib library [http://www.alglib.net/]

There is a Laravel Lumen RESTful API written on top of that Python XML RPC endpoint to extend functionality out in a more flexible platform. This RESTful API is called Sodium.

## Installation
1. First thing first, clone this repo down
2. Next, you'll want to download a copy of the CPython build of AlgLib, currently versioned at 3.14.0 as of this date.  Find the link here: [http://www.alglib.net/download.php]
3. Extract the file, you'll be left with a 'cpython' folder; move that folder into the root repo folder you just cloned.
4. Build the AlgLib CPython implimentation by running:
```
cd cpython
sudo python3 ./setup.py install
```
This will compile and build the AlgLib library and install it system-wide.
5. Next, install the python-daemon module with...
```
sudo pip3 install python-daemon
```
6. Start the Iodine XML RPC Server by running...
```
sudo python3 ./server3.py -s
```

## Tests
There is a simple connection test file included, check.py, that checks for proper AlgLib CPython import and a basic uptime RPC test

## TODO
* Still need to add Co to the computation grid...
* Ken, whatever you're thinking, don't include oxides and other bonds in the computation grid...convert oxides into available forms before sending to XML RPC, otherwise molecular composition will be different
