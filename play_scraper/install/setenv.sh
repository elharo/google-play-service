#!/bin/sh
# get this script's location
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )

# list of apt-get applications to install
LIST_OF_APPS="build-essential tcl8.5 git python-dev python-pip python-lxml openjdk-7-jdk screen"

# list of python pip libraries to install
LIST_OF_PY_LIBS="redis pyquery"

# Install defined LIST_OF_APPS
sudo apt-get update
sudo apt-get install -y ${LIST_OF_APPS}

# Install Redis (from source)
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
sudo update-rc.d "redis_${redisPort}" defaults

# Install python libs
sudo pip-2.7 install ${LIST_OF_PY_LIBS}
sudo pip-2.7 install https://pypi.python.org/packages/source/s/selenium/selenium-2.37.0.tar.gz

# Install selenium server
cd ~/
mkdir /usr/lib/selenium/
cd /usr/lib/selenium/
sudo wget http://selenium-release.storage.googleapis.com/2.40/selenium-server-standalone-2.40.0.jar
mkdir -p /var/log/selenium/
chmod a+w /var/log/selenium/
cd ${SCRIPTPATH}
sudo cp selenium /etc/init.d/
chmod 755 /etc/init.d/selenium
sudo /etc/init.d/selenium start
sudo update-rc.d selenium defaults

# Install Phantom JS
cd /usr/local/share/
sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2
sudo tar jxvf phantomjs-1.9.7-linux-x86_64.tar.bz2
sudo ln -s /usr/local/share/phantomjs-1.9.7-linux-x86_64/ /usr/local/share/phantomjs
sudo ln -s /usr/local/share/phantomjs/bin/phantomjs /usr/local/bin/phantomjs
which phantomjs

# Back to home dir
cd ~/

# Env setup completed
echo "***** environment setup for indexer engine completed *****"