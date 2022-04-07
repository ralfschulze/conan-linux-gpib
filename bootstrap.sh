#!/bin/sh
mkdir -p build
python3 -m venv venv || exit 1
. ./venv/bin/activate
python3 -m ensurepip
python3 -m pip install --require-virtualenv wheel || exit 1
python3 -m pip install --require-virtualenv -I -r requirements.txt