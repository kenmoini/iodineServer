# iodineServer
Iodine - An application that serves the computation needs of Salt Smarts

## Introduction
Iodine is the name of the server application that processes fertilizer computation formulae sent from the Salt Smarts platform.
It is a simple XML RPC server written in Python that extends the CPython build of the AlgLib library [http://www.alglib.net/]
There is a Laravel Lumen RESTful API written on top of that Python XML RPC endpoint to extend functionality out in a more flexible platform.

## Installation
-First thing first, clone this repo down
-Next, you'll want to download a copy of the CPython build of AlgLib, currently versioned at 3.14.0 as of this date.  Find the link here: [http://www.alglib.net/download.php]
-Extract the file, you'll be left with a 'cpython' folder; move that folder into the root repo folder you just cloned.
-Build the AlgLib CPython implimentation by running:
```
cd cpython
sudo python3 ./setup.py install
```
This will compile and build the AlgLib library and install it system-wide.
-Next, install the python-daemon module with...
```
sudo pip3 install python-daemon'
```

