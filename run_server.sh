#!/bin/bash
 
# directory of this script
DIR=$(cd $(dirname "$0"); pwd)

cd $DIR

export PYTHONPATH=$DIR
export PATH=$DIR/env/bin

exec uwsgi --socket 127.0.0.1:8080 -w wsgi:application