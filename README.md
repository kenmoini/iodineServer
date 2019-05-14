# iodineServer
Iodine - An application that serves the Linear Algebraic computation needs of Salt Smarts via an XML-RPC endpoint.

## Introduction
Iodine is the name of the server application that processes fertilizer computation formulae sent from the Salt Smarts platform.

It is a simple XML RPC server written in Python that extends the CPython build of the AlgLib library [http://www.alglib.net/]

There is a Laravel Lumen RESTful API written on top of this Python XML RPC endpoint to extend functionality out in a more flexible platform. This RESTful API is called Sodium.

Iodine is deployed/installed easily via a Bash script, Dockerfile, or Jenkinsfile, with an available Supervisord configuration file in order to provide on-boot starting of the Iodine Server as well as monitoring of the process.

## Requirements
Ideally this should be deployed in a small VPS/VM, or in a container.  There is a **Dockerfile** that will create a container with this running, as well as a **Jenkinsfile** for inclusion into a CI/CD pipeline with **Red Hat OpenShift**.

Otherwise, this will require...
- Debian/Ubuntu, or RHEL/CentOS/Fedora
- Python 2.7 (EW!)

## Installation (as root/sudoer)
1. First thing first, clone this repo down - ideally do so under /opt so that the Supervisor configuration works without modifcation:
```
root@localhost:/opt# git clone https://github.com/kenmoini/iodineServer.git
```
2. Next, you'll just need to run the **install.sh** file:
```
root@localhost:/opt# cd iodineServer
root@localhost:/opt/iodineServer# ./install.sh
```
3. You can run a quick test...
```
root@localhost:/opt/iodineServer# python ./check.py
```
4. And then run the server!
```
root@localhost:/opt/iodineServer# python ./xmlrpc-server.py
```
5. (Optional) Install Supervisord Configuration
The **install.sh** script installs Supervisord but you still need to move the configuration, and maybe modify it if you did not clone this repo into your /opt directory.
```
root@localhost:/opt/iodineServer# cp iodine-supervisord.conf /etc/supervisor/conf.d/
```

## Tests
There is a simple connection test file included, **check.py**, that checks for proper AlgLib CPython import, a basic uptime RPC test, as well as a verified fertilizer computation test.

## Notes
* This requires Python 2.7...there are additional scripts in this repo that have been attempts at modernizing to Python 3 and RESTful APIs instead of the XML-RPC layer, but I'm not the best Python programmer...open-source community...halp?
* To start this Iodine Server 

## TODO
* Still need to add Co to the computation grid...
* Ken, whatever you're thinking, don't include oxides and other bonds in the computation grid...convert oxides into available forms before sending to XML RPC, otherwise molecular composition will be different
* Attempt moving to Python 3 again...
* Integrate AlgLib directly with Flask REST API module, but AlgLib doesn't like how data is passed...
