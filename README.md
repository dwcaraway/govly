Evented
=================
Welcome to Evented, an event aggregation framework. 

Installation
---------------
Install Python 2.7.x, pip and virtualenv
```
$ sudo apt-get update
$ sudo apt-get install python2.7 python-setuptools libxml2-dev libxslt-dev python-dev lib32z1-dev
$ sudo easy_install pip
$ sudo pip install virtualenv
```
** Note ** mac users should run ``` xcode-select --install``` for libxml support

Next, install Bower and Grunt
```
$ sudo apt-get install nodejs
$ sudo npm install -g bower grunt
```

Git clone this repository
```
$ git clone /url/to/this.git /path/to/this
```

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

Now in the /path/to/this directory, install the client side (javascript) requirements with bower. This creates an app/statc/js/bower_components directory with all the javascript dependencies.
```
$ bower install
```

Now install the Grunt build dependencies
```
$ npm install
```

To launch the server
```
$ python run.py
```

Running tests
------------
First, install the test requirements
```
$ pip install -r test-requirements.txt
```

To run tests, navigate to the tests folder. Functional tests are in /functional while unit tests are in /unit. 
```
$ nosetests
```

To run client-side functional tests, first install nodejs and then PhantomJS
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
