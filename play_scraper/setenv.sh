#!/bin/sh
LIST_OF_APPS="build-essential tcl8.5 python-dev python-pip python-lxml openbox firefox xrdp"
LIST_OF_PY_LIBS="redis selenium pyquery"

# Install defined LIST_OF_APPS
sudo apt-get update
sudo apt-get install -y ${LIST_OF_APPS}

# Install redis
cd ~/
wget http://download.redis.io/releases/redis-2.8.3.tar.gz
tar -xvzf redis-2.8.3.tar.gz
rm redis-2.8.3.tar.gz
cd redis-2.8.3
make
make test
sudo make install
cd utils
sudo ./install_server.sh
echo -n "Please enter the desired port for redis [default = 6379]: ";
read redisPort;

# updare demon according to the above details
sudo update-rc.d "redis_${redisPort}" defaults

# Install python libs
sudo pip install ${LIST_OF_PY_LIBS}

# Env setup completed
echo "Env setup completed"