#!/bin/bash

#change directory to scripts location
cd "${0%/*}"
#to the dependency folder
cd ./dep

#install python dependencies

#bottle
echo -e "\e[1;34minstall bottle\e[0m"
cd bottle
python3 setup.py install --user

#redis-py
echo -e "\e[1;34minstall redis-py\e[0m"
cd ../redis-py
python3 setup.py install --user

#waitress
echo -e "\e[1;34minstall waitress\e[0m"
cd ../waitress
python3 setup.py install --user


#checking for redis-server as prerequisite
REDIS_LOCATION="$(which redis-server)"
if [ -f $REDIS_LOCATION ]; then
  REDIS_PID="$(pgrep redis-server)"
  if [ !=$REDIS_PID ]; then
    echo -e "\e[1;33mredis-server is up already\e[0m"
  else
    echo -e "\e[1;33mstarting redis-server...\e[0m"
    redis-server &
  fi
else
  echo -e "\e[1;31m install redis-server first\e[0m"
  echo -e "\e[1;31m search and install redis.x86_64 \e[0m"
  exit 1
fi

#changing to source directory
cd ../../

echo -e "\e[1;96mreseting all stat params..\e[0m"
python3 redis_parameter_init.py > /dev/null &

UPDATER="$(pgrep -a python | grep redisServer_Updater.py | cut -d ' ' -f1)"
if [ "x$UPDATER"!="x" ]; then
  echo -e "\e[1;96mMonitoring and Updating process is  already up\e[0m"
else
  echo -e "\e[1;96mMonitoring and Updating params..\e[0m"
  python3 redisServer_Updater.py > /dev/null &
fi
