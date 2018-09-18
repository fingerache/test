#!/bin/bash

#script for running all the required web services

STATSCTRLLR="$(pgrep -a python | grep statsController.py | cut -d ' ' -f1)"
PROCSCTRLLR="$(pgrep -a python | grep processController.py | cut -d ' ' -f1)"

if [ "x$STATSCTRLLR" != "x" ]; then
    echo -e "\e[1;38;5;35mstatsController is already running at http://localhost:2526 PID:${STATSCTRLLR}\e[0m"
else
    echo -e "\e[1;38;5;35mstarting statsController at http://localhost:2526... \e[0m"
    python3 statsController.py > /dev/null & 
fi


if [ "x$PROCSCTRLLR" != "x" ]; then
    echo -e "\e[1;38;5;35mprocessController is already running at http://localhost:2525 PID:${PROCSCTRLLR}\e[0m"
else
    echo -e "\e[1;35m starting processController at http://localhost:2525... \e[0m"
    python3 processController.py > /dev/null &
fi