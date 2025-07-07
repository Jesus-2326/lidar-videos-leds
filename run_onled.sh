#!/bin/bash

VENV_PATH="$HOME/Desktop/lidar-videos-leds/venv"
PYTHON="$VENV_PATH/bin/python"
SITE_PACKAGES="$VENV_PATH/lib/python3.11/site-packages"

sudo VIRTUAL_ENV=$VENV_PATH PYTHONPATH=$SITE_PACKAGES $PYTHON onled.py
