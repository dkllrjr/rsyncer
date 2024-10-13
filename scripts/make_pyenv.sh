#!/bin/bash

python3.11 -m venv ../pyenv
source ../pyenv/bin/activate
python3 -m pip install --upgrade build twine
