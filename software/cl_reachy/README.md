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
python -m cl_reachy.controller.visual
```

### Speech Synthesis
Says the message from a say message.
```bash
python -m cl_reachy.view.sound.speechsynthesis
```

### Body
Currently interfaces with the simulator. Accepts messages for sample, preset motions.
```bash
python -m cl_reachy.view.body.body
```

### Audio
```bash
python -m cl_reachy.controller.audio
```

### Main Controller
```bash
python -m cl_reachy.controller.main
```
