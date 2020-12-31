# CL Reachy

## Anaconda
### Set up your Anaconda environment
If you don't have Anaconda installed, download the correct version for you computer from here:
https://www.anaconda.com/products/individual

In this directory, run the following command to create your Reachy python environment:
```bash
conda env create -f environment.yml
```

### Activate your environment
```bash
conda activate reachy-env
```

### Deactivate your environment
```bash
conda deactivate
```

## Mosquitto (MQTT)
If you don't have Docker installed, download the correct version for your computer from here:
https://www.docker.com/products/docker-desktop


### Starting the message queue
```bash
docker run -it --name mosquitto1 -p 1883:1883 eclipse-mosquitto
```

### Stopping the message queue
Press control-c twice in the window that Mosquitto is running in.

## Optional: MQTT.FX
This is a gui client for MQTT.  You can use it to debug messages on the message queue.
https://mqttfx.jensd.de/index.php/download

## Running nodes
These are the following nodes that are available.  To start them, run each of them in a separate terminal in this directory in the reachy-env Anaconda environment.

### Logger
Simple logger. Receives log messages from other nodes.
```bash
python -m cl_reachy.view.logger
```

### Console
Command line utility to test sending messages to other nodes.
```bash
python -m cl_reachy.view.console
```

### Camera
Takes a picture from your webcam.
```bash
python -m cl_reachy.controller.visual.main --env=[reachy|dev]
```

If you are using VirtualBox, you will need to set up the webcam passthru:
https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/webcam-passthrough.html
For Mac OS:
List available webcams
```bash
VBoxManage list webcams
```
You should see something like:
```bash
$ VBoxManage list webcams
Video Input Devices: 1
.1 "FaceTime HD Camera"
CC2617300VLG1HNBK
```
To attach the FaceTime HD Camera, do:
```bash
VBoxManage controlvm reachy-dev webcam attach .1
```

### Speech Synthesis
Says the message from a say message.
```bash
python -m cl_reachy.view.sound.speechsynthesis.main --env=[reachy|dev]
```

### Body
Currently interfaces with the simulator. Accepts messages for sample, preset motions.
```bash
python -m cl_reachy.view.body.main --env=[reachy|dev]
```

### Threshold
Triggers based on sound threshold
```bash
python -m cl_reachy.view.sound.threshold.main --env=[reachy|dev]
```

### Wakeword
Triggers on the wake word, "Reachy"
```bash
python -m cl_reachy.view.sound.wakeword.main --env=[reachy|dev]
```

### Speech Recognition
Listens and transcribes spoken words
#### Google Cloud
```
python -m cl_reachy.view.sound.speechrecognition.google.main
```
or
#### Mozilla Deep Speech
```
python -m cl_reachy.view.sound.speechrecognition.mozilla.main --env=[reachy|dev]
```

### Main Controller
```bash
python -m cl_reachy.controller.main
```
