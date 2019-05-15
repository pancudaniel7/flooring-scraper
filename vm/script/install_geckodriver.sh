#!/usr/bin/env bash

sudo apt-get update -y

wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
sudo tar -xvzf geckodriver*
sudo chmod +x geckodriver
sudo mv geckodriver /usr/bin/