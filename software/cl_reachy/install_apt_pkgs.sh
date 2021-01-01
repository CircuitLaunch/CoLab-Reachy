#!/usr/bin/bash

# utilities
apt-get install screen htop less zip unzip -y

# editors
apt-get install emacs vim -y

# rdp
apt-get install xrdp -y
adduser xrdp ssl-cert

# cheese
apt-get install cheese -y

# mosquitto
apt-get install software-properties-common -y
apt-get update
apt-get install mosquitto mosquitto-clients -y
apt clean

# swig
apt-get install -y swig

# sound
apt-get install libpulse-dev -y
apt-get install libasound2-dev -y
apt-get install pavucontrol -y
apt-get install libmpg123-dev mpg123 -y

# coral tpu
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-get update
apt-get install libedgetpu1-std -y

# numpy dependencies
apt-get install libatlas-base-dev -y

# opencv dependencies
apt-get install python3-h5py
