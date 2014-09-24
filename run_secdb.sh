#!/bin/bash
 
# directory of this script
DIR=$(cd $(dirname "$0"); pwd)
 
cd $DIR
 
export PYTHONPATH=$DIR/lib
export PATH=$DIR/../venv/bin
 
exec python $DIR/run.py
