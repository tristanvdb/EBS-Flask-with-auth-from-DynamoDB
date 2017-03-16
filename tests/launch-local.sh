#!/bin/bash -e

basedir=$(realpath $(dirname $0)/..)

[ -z $1 ] && exit 1

if [ ! -e $basedir/.venv ]; then
  virtualenv $basedir/.venv
fi

source $basedir/.venv/bin/activate

pip install -r $basedir/requirements.txt

export PYTHONPATH=$basedir

export SERVER_SERVICE=$1
export AWS_PROFILE=$2
export AWS_REGION=$3

[ -z $AWS_REGION ] && AWS_REGION='us-east-1'

python $basedir/scripts/create.py --service-name $SERVER_SERVICE

python $basedir/scripts/wsgi.py

deactivate

