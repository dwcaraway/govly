Vitals
=================
Welcome to Vitals, a market research tool for the federal government marketplace.

Architecture
---------------
Vitals consists of a static AngularJS application client connected to Python Flask-based data and services on the
backend via a Hypermedia Application Language (HAL) REST interface.

Installation (Server)
---------------------
Install Python 2.7.x, pip and virtualenv
```
$ sudo apt-get update
$ sudo apt-get install python2.7 python-setuptools libxml2-dev libxslt-dev python-dev lib32z1-dev
$ sudo easy_install pip
$ sudo pip install virtualenv
```
** Note ** mac users should run ``` xcode-select --install``` for libxml support

Create and activate the virtual environment
```
mkdir /path/to/this/env
cd env
virtualenv . --no-site-packages
source bin/activate
```
you should now see a ```(env)``` in front of your terminal entry

Now in the /path/to/this directory, install the requirements
```
cd /path/to/this
$ pip install -r requirements.txt
```

To launch a development server, run the below. _NOTE: DO NOT USE BUILT-IN SERVER FOR PRODUCTION_
```
$ python manage.py runserver
```

Installation (Client)
---------------------
The client side is static and can be loaded directly into a server or deployed via a CDN.

Install Bower and Grunt
```
$ sudo apt-get install nodejs
$ sudo npm install -g bower grunt
```

Now in the /path/to/this directory, install the client side (javascript) requirements with bower. This creates an app/statc/js/bower_components directory with all the javascript dependencies.
```
$ bower install
```

Now install the Grunt build dependencies
```
$ npm install
```

Running Tests
------------

(Server-Side)

First install the test requirements
```
$ pip install -r test-requirements.txt
```

To run tests
```
$ python manage.py test
```

(Client Side)

To run client-side functional tests, install
```
$ sudo apt-get update
$ sudo apt-get install nodejs
$ sudo ln -s /usr/bin/nodejs /usr/bin/node
$ sudo npm install -g phantomjs
```

Then create a directory for the phantomJS output
```
$ sudo mkdir /var/log/phantomJS
$ sudo chown yourusername /var/log/phantomJS
```
