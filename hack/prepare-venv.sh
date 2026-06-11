#!/usr/bin/env bash

# initialize and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# install needed modules inside the virtual environment
python3 -m pip install -r requirements.txt
