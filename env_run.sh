#!/bin/bash
# Runs any command (the args) in the virtualenv environment where this script
# resides.
# You need to change the ACTIVATE_PATH variable
# depending on where your virtualenv activate file is relative to this script.
# The WORKING_DIR var controls the directory from which the command will be run.
# I put this in a bin folder at the top level of my app.
# my virtualenv structure:
# /codingbooth_env
# /codingbooth_env/bin  ( with the venv activate script )
# /codingbooth_env/codingbooth
# /codingbooth_env/codingbooth/env_run.sh (this script)
#
# use: /path/to/env_run.sh <command>
# e.g.: /path/to/env_run.sh python main.py --arg-one --arg-two

ACTIVATE_PATH=../bin/activate
MY_PATH="`dirname \"$0\"`"              # relative
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized

cd ${MY_PATH}
source ${ACTIVATE_PATH}
exec $@
