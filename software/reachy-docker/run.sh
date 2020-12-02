#!/bin/bash

dbus-launch&

# start xrdp
service xrdp start&

# start mosquitto
sudo service mosquitto start&

su - reachyuser -c "/bin/bash /tmp/run_reachy.sh"&

tail -f /var/log/xrdp.log