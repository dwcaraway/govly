Security Dashboard
=================
Welcome to the Security Dashboard project, a web application for monitoring and protecting your network resources.

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

Now in the /path/to/this directory, install the client side (javascript) requirements with bower. This creates an app/bower_components directory with all the javascript dependencies.
```
$ bower install
```

Install the [Java JDK](http://www.oracle.com/technetwork/java/javase/downloads/index.html). We require version 1.7 or later


Now install the Neo4j graph database
```
$ sudo apt-get install neo4j && neo4j start
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

To run Behavior Driven Tests, in the ```tests``` folder, run
```
$ behave
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
