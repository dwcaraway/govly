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

To create the (empty) database tables

    $ python manage.py db upgrade


To create and populate the database tables with canned data

    $ python manage.py db recreate


## Run the Development Server
To launch a development server, run the below. _NOTE: DO NOT USE BUILT-IN SERVER FOR PRODUCTION_
```
$ python manage.py runserver
```

Installation (Client)
---------------------
The client side is static and can be loaded directly into a server or deployed via a CDN.

Install the latest NodeJS(you might needs to use a PPA or compile from source to get the latest nodejs)

Install Grunt and Bower
```
$ sudo npm install -g bower grunt
```

Now in the /path/to/this directory, install the client side (javascript) requirements with bower. This creates an app/statc/js/bower_components directory with all the javascript dependencies.
```
$ bower install
```

Now install the build dependencies
```
$ npm install
```

Running Tests
------------

(Server-Side)

First install the test requirements
```
$ pip install -r requirements/develop.txt
```

On Mac, if you receive a message that 'ffi.h' not found, follow [stackoverflow directions](http://stackoverflow.com/questions/22875270/error-installing-bcrypt-with-pip-on-os-x-cant-find-ffi-h-libffi-is-installed)
On Mac, if you receive a message that 'libxml/xmlversion.h' is missing, install lxml alone with static library ```STATIC_DEPS=true pip install lxml```
I also read that you may want to install ```xcode-select --install```

To run tests
```
$ python manage.py test
```

(Client Side)

To run client-side tests
```
$ grunt test
```

Primary Grunt Tasks
-------------------
##Build
*  **build:local** or **build (default)**: Build files to dist folder ready for deployment on host which also contains the api (localhost:5000). Used for development only.
*  **build:staging**: Build files to dist folder ready for staging deployment on CDN. Built files will assume the api is at https://staging-api.fogmine.com
*  **build:production**: Build files to dist folder ready for production deployment on CDN. Built files will assume the api is at https://api.fogmine.com

##Serve
*  **serve:mock** or **serve (default)**: Starts a grunt server on localhost:9000 with live reload connected to angular source files.. mock backend is used.
*  **serve:local**: Same as serve:mock except an api is expected on localhost:5000
*  **serve:dist**: Serves whatever is in the dist folder (depends on which build task was run) on localhost:9000

Database Migrations
-------------------
Modifications to the database should be performed through migrations. The general process is

1.  Update the SQLAlchemy models with any changes that you wish to make
2.  Generate database migration revision file ```python manage.py db migrate```
3.  Edit the generated migration file to ensure that downgrade and upgrade functions are properly defined. Upgrades move forward in time while downgrads are backwards in time.
4.  Verify migration completes successfully by ```python manage.py db upgrade```.
5.  Verify migration downgrade completes by ```python manage.py db downgrade```. Repeat step 4 to get back to upgraded state.

Deploying
---------
To deploy to staging, simply push your changes to the "master" branch in Bitbucket. If the build passes then you'll be able to view the results at
https://staging.dash.fogmine.com

To deploy to production, you push your changes to the "production" branch. *Due to a Bitbucket bug, you need to use ```--no-ff``` for merges
from master to production in order to generate a change event and trigger the build.
