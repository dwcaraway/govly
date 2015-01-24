Vitals
=================
Welcome to Vitals, a market research tool for the federal government marketplace.

Architecture
---------------
Vitals consists of a static AngularJS application client connected to Python Flask-based data and services on the
backend via a Hypermedia Application Language (HAL) REST interface.

Installation (Server)
---------------------
Install Python 2.7.x, pip, virtualenv
```
$ sudo apt-get update
$ sudo apt-get install python2.7 python-setuptools libxml2-dev libxslt-dev python-dev postgresql-server-dev-9.3
$ sudo easy_install pip
$ sudo pip install virtualenv
```
** Note ** mac users should run ``` xcode-select --install``` for libxml support

Install [Redis](http://vvv.tobiassjosten.net/linux/installing-redis-on-ubuntu-with-apt/) -- TODO add instructions
Install PostGreSQL -- TODO need instructions

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

## Configure the Database
Install Postgresql 9.3+

    sudo apt-get install postgresql-9.3

Configure the pg_hba.conf file on your system (location varies) to allow local connections without passwords. Your hba.conf should have lines like below


local all all trust
host all all 127.0.0.1/32 trust

Create the database and role within your system user name

    $ psql -c 'create user vitals password 'vitals';' -U postgres
    $ psql -c 'CREATE DATABASE vitalsdev WITH OWNER vitals;' -U postgres


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
