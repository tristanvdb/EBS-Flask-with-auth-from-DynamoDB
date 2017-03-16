#!/bin/bash -e

basedir=$(realpath $(dirname $0)/..)

mkdir -p $basedir/.venv

virtualenv $basedir/.venv > $basedir/.venv/virtualenv.log

source $basedir/.venv/bin/activate

pip install -r $basedir/requirements.txt > $basedir/.venv/pip-install.log

deactivate

echo -e "\nexport PYTHONPATH=$basedir:\$PYTHONPATH" >> $basedir/.venv/bin/activate

echo "VirtualEnv created: $basedir/.venv"

