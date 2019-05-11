#!/usr/bin/env bash

#python3 tools
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo pip install --upgrade pip
sudo pip3 install virtualenv

#phantomjs
sudo apt-get install build-essential chrpath libssl-dev libxft-dev libfreetype6-dev libfreetype6 libfontconfig1-dev libfontconfig1 -y
sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/
sudo rm phantomjs-2.1.1-linux-x86_64.tar.bz2
sudo ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/
phantomjs --version

#firefox
sudo apt upgrade
sudo apt install firefox


#create venv
virtualenv -p /usr/bin/python3.6 venv

#activate venv
source venv/bin/activate

#install requirements
venv/bin/python3.6 install -r requirements.txt