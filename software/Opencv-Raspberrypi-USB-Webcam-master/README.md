# Requirments for this projects


# Software Requirments 
Raspbian jessie,

Opencv 



# Hardware Requirments 



Raspberry pi,

USB Webcam



# Using the Raspbian Provided OpenCV Pre-compiled Binaries #


Raspbian includes OpenCV precompiled binaries, which as of the most recent release are only moderately out of date (OpenCV 2.4.9).  At a RPi command line enter the following:

$ dpkg -l | less

This will list all installed packages.  Navigate to the opencv libs and you will see the version of the OpenCV libraries included with the current Raspbian build is 2.4.9, which was released in April of 2014.  If you would like to use these pre-compiled binaries, proceed as follows at the RPi command line :

$ sudo apt-get update

$ sudo apt-get upgrade

$ sudo apt-get install libopencv-dev python-opencv

# verify the OpenCV install

$ python

>>> import cv2

>>> cv2.__version__  

## will say "2.4.9" if pre-compiled binary installation was successful

## Now you can clone or download my project and run 'smile_detection.py' see smile and face detection on your webcam
## make sure you are running this project in 'python 2 (IDLE)' on your raspbian jessie becouse its version "2.4.9"


To Run any appliction on Auto start on boot of raspberry Pi 
Just Open file:
$ sudo nano /etc/profile
and at the end add you command line than save and exit and restart your pi
