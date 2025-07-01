#!/bin/bash
source venv/bin/activate
sudo env "PATH=$PATH" "VIRTUAL_ENV=$VIRTUAL_ENV" "PYTHONPATH=$PYTHONPATH" "$VIRTUAL_ENV/bin/python" lidarVideosLeds5.py
